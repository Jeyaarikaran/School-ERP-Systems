"""Pure Domain Engine for Exam Result Calculation.

This module accesses no databases and performs no IO. It relies entirely on provided
data structures (grading systems, bands, raw marks) to deterministically output
computed results, rankings, and GPAs using Decimal precision.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List, Optional
from collections import defaultdict


class MarksCalculationEngine:
    """Computes exam results and ranks from raw marks and grading data."""

    @staticmethod
    def _round(value: Decimal) -> Decimal:
        """Rounds to 2 decimal places using HALF_UP strategy."""
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
    @staticmethod
    def calculate_percentage(obtained: Decimal, max_marks: Decimal) -> Decimal:
        if max_marks == Decimal(0):
            return Decimal(0)
        return MarksCalculationEngine._round((obtained / max_marks) * Decimal(100))

    @staticmethod
    def find_grade(percentage: Decimal, grading_bands: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Locates the correct grade band for an UNROUNDED percentage.
        Bands are half-open [min, max) except when max == 100 which is [min, max].
        """
        for band in grading_bands:
            min_p = Decimal(str(band["min_percent"]))
            max_p = Decimal(str(band["max_percent"]))
            
            # The top band includes 100 explicitly
            if max_p == Decimal("100") and min_p <= percentage <= max_p:
                return band
            # Other bands are [min, max)
            elif min_p <= percentage < max_p:
                return band
                
        return None

    @staticmethod
    def compute_student_subject(
        student_id: str,
        subject_id: str,
        marks: List[Dict[str, Any]], 
        components: List[Dict[str, Any]], 
        grading_system: Dict[str, Any],
        scoring_type: str = "numeric" # "numeric" or "grade_only"
    ) -> Dict[str, Any]:
        """
        Computes total, percentage, and pass/fail for a single student on a single subject.
        """
        bands = grading_system.get("bands", [])
        
        # Output structure
        result = {
            "student_id": student_id,
            "subject_id": subject_id,
            "total_obtained": None,
            "total_max": None,
            "percentage": None,
            "grade": None,
            "grade_point": None,
            "is_pass": True,
            "scoring_type": scoring_type
        }
        
        # If grade_only, it doesn't contribute to totals
        if scoring_type == "grade_only":
            # Just take the grade from the first component's mark
            if marks and marks[0].get("grade_label"):
                result["grade"] = marks[0]["grade_label"]
                # Determine pass/fail based on grading system bands if they match, else default pass
                band = next((b for b in bands if b["grade_label"] == result["grade"]), None)
                if band and band.get("is_fail"):
                    result["is_pass"] = False
            return result

        # Compute Numeric Subject
        total_obtained = Decimal(0)
        total_max = Decimal(0)
        is_pass = True
        
        comp_map = {str(c["id"]): c for c in components}
        
        for mark in marks:
            status = mark["attendance_status"]
            comp = comp_map[str(mark["component_id"])]
            comp_max = Decimal(str(comp["max_marks"]))
            comp_pass = Decimal(str(comp["pass_marks"]))
            
            if status == "absent":
                # Counts as 0 obtained, full max, and fails the subject if must_pass
                total_max += comp_max
                if comp.get("must_pass", True):
                    is_pass = False
            elif status == "exempt":
                # Excluded from both max and obtained
                continue
            elif status == "withheld":
                # Withheld completely invalidates numeric calculations for this subject
                result["is_pass"] = False
                result["total_obtained"] = None
                return result
            else:
                # Present
                obtained = Decimal(str(mark.get("marks_obtained") or 0))
                total_obtained += obtained
                total_max += comp_max
                
                if comp.get("must_pass", True) and obtained < comp_pass:
                    is_pass = False
                    
        if total_max == 0:
            # Entirely exempt
            return result
            
        result["total_obtained"] = total_obtained
        result["total_max"] = total_max
        percentage = MarksCalculationEngine.calculate_percentage(total_obtained, total_max)
        result["percentage"] = percentage
        
        # Overall subject pass check
        sub_pass_percentage = Decimal(str(grading_system.get("pass_percentage", 0)))
        if percentage < sub_pass_percentage:
            is_pass = False
            
        result["is_pass"] = is_pass
        
        # Assign Grade
        grade_band = MarksCalculationEngine.find_grade(percentage, bands)
        if grade_band:
            result["grade"] = grade_band["grade_label"]
            result["grade_point"] = Decimal(str(grade_band["grade_point"]))
            
        return result


    @staticmethod
    def compute_student_overall(
        student_id: str,
        subject_results: List[Dict[str, Any]],
        subject_weights: Dict[str, Decimal],
        mandatory_subjects: set,
        grading_system: Dict[str, Any],
        overall_pass_rule: str = "all_mandatory" # or "percentage_only"
    ) -> Dict[str, Any]:
        """
        Aggregates subject results into an overall percentage, GPA, and Result status.
        """
        bands = grading_system.get("bands", [])
        
        result = {
            "student_id": student_id,
            "total_obtained": Decimal(0),
            "total_max": Decimal(0),
            "percentage": None,
            "overall_grade": None,
            "gpa": None,
            "overall_result": "pass"
        }
        
        total_gpa_points = Decimal(0)
        total_gpa_weights = Decimal(0)
        
        # Check for withheld or missing mandatory
        has_withheld = any(sr.get("attendance_status") == "withheld" or sr.get("total_obtained") is None for sr in subject_results if sr["scoring_type"] == "numeric")
        if has_withheld:
            result["overall_result"] = "withheld"
            return result
            
        completed_subjects = {sr["subject_id"] for sr in subject_results}
        missing_mandatory = mandatory_subjects - completed_subjects
        if missing_mandatory:
            result["overall_result"] = "incomplete"
            return result
            
        # Aggregate numeric subjects
        numeric_results = [sr for sr in subject_results if sr["scoring_type"] == "numeric"]
        
        if not numeric_results:
            result["overall_result"] = "incomplete"
            return result
            
        for sr in numeric_results:
            result["total_obtained"] += sr["total_obtained"]
            result["total_max"] += sr["total_max"]
            
            weight = subject_weights.get(sr["subject_id"], Decimal("1.0"))
            if sr.get("grade_point") is not None:
                total_gpa_points += sr["grade_point"] * weight
                total_gpa_weights += weight
                
        # Calculate overall percentage
        percentage = MarksCalculationEngine.calculate_percentage(result["total_obtained"], result["total_max"])
        result["percentage"] = percentage
        
        # Calculate GPA
        if total_gpa_weights > 0:
            result["gpa"] = MarksCalculationEngine._round(total_gpa_points / total_gpa_weights)
            
        # Assign Overall Grade
        grade_band = MarksCalculationEngine.find_grade(percentage, bands)
        if grade_band:
            result["overall_grade"] = grade_band["grade_label"]
            
        # Determine overall pass/fail
        if overall_pass_rule == "all_mandatory":
            failed_mandatory = any(
                not sr["is_pass"] 
                for sr in subject_results 
                if sr["subject_id"] in mandatory_subjects
            )
            if failed_mandatory:
                result["overall_result"] = "fail"
        elif overall_pass_rule == "percentage_only":
            pass_pct = Decimal(str(grading_system.get("pass_percentage", 0)))
            if percentage < pass_pct:
                result["overall_result"] = "fail"
                
        return result

    @staticmethod
    def apply_competition_ranking(overall_results: List[Dict[str, Any]]) -> None:
        """
        Applies standard competition ranking (1, 2, 2, 4) in-place.
        Only 'pass' or 'fail' results are ranked. 'incomplete' and 'withheld' are unranked.
        Sorted by percentage descending.
        """
        # Filter rankable students
        rankable = [r for r in overall_results if r["overall_result"] in ("pass", "fail") and r.get("percentage") is not None]
        
        # Sort descending by percentage
        rankable.sort(key=lambda x: x["percentage"], reverse=True)
        
        current_rank = 1
        for i, res in enumerate(rankable):
            if i > 0 and res["percentage"] == rankable[i-1]["percentage"]:
                res["rank"] = rankable[i-1]["rank"]
            else:
                res["rank"] = current_rank
                
            current_rank += 1
            
        # Ensure unranked get None
        for res in overall_results:
            if res["overall_result"] not in ("pass", "fail") or res.get("percentage") is None:
                res["rank"] = None
