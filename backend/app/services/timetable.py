"""Timetable Core Services and Conflict Logic."""

from datetime import date
from typing import Any, Dict, List

def calculate_overlap_claims(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Given a list of timetable entries, generates the physical claims that 
    the database will enforce via EXCLUDE USING gist constraints.
    """
    claims = []
    for entry in entries:
        base = {
            "timetable_id": entry["timetable_id"],
            "entry_id": entry["id"],
            "weekday": entry["weekday"],
            "period_id": entry["period_id"],
            # effective_range would be translated to a daterange string by the ORM
            "effective_range": f"[{entry['effective_from']},{entry.get('effective_to', '')})"
        }
        
        # 1. Teacher claim
        claims.append({**base, "resource_type": "teacher", "resource_id": entry["teacher_id"]})
        
        # 2. Section claim
        claims.append({**base, "resource_type": "section", "resource_id": entry["section_id"]})
        
        # 3. Room claim (if assigned)
        if entry.get("room_id"):
            claims.append({**base, "resource_type": "room", "resource_id": entry["room_id"]})
            
    return claims


class TimetableEngine:
    @staticmethod
    def validate_draft(entries: List[Dict[str, Any]], assigned_teachers: set, class_subjects: set) -> List[Dict[str, Any]]:
        """
        Pure function to validate a draft timetable against soft and hard constraints.
        """
        errors = []
        # Check teacher assignments
        for entry in entries:
            t_assignment = (entry["section_id"], entry["subject_id"], entry["teacher_id"])
            if t_assignment not in assigned_teachers:
                errors.append({
                    "entry_id": entry.get("id"),
                    "code": "TEACHER_NOT_ASSIGNED",
                    "message": "Teacher is not assigned to this subject for this section."
                })
            
            c_subject = (entry["class_id"], entry["subject_id"])
            if c_subject not in class_subjects:
                errors.append({
                    "entry_id": entry.get("id"),
                    "code": "SUBJECT_NOT_IN_CLASS",
                    "message": "Subject is not part of the class syllabus."
                })
        
        return errors
