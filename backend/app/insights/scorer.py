"""Risk Scoring Engine — Pure, transparent risk rules."""

from decimal import Decimal
from typing import Any, Dict


class RiskFactor(Dict[str, Any]):
    rule: str
    value: float
    threshold: float
    weight: int
    contribution: int


class RiskScorer:
    """Computes transparent student risk scores from pure data."""

    @staticmethod
    def evaluate(student_data: dict[str, Any]) -> dict[str, Any]:
        """
        Evaluates risk based on attendance, behavior, and academic data.
        Does NOT include financial data (fees) per ADR.
        """
        score = 0
        factors: list[RiskFactor] = []

        # 1. Attendance Rule (Weight: 40)
        attendance_pct = student_data.get("attendance_percentage")
        if attendance_pct is not None and attendance_pct < 75.0:
            contribution = 40
            score += contribution
            factors.append({
                "rule": "attendance_below_threshold",
                "value": float(attendance_pct),
                "threshold": 75.0,
                "weight": 40,
                "contribution": contribution
            })

        # 2. Academic Trend Rule (Weight: 35)
        failing_subjects = student_data.get("failing_subjects_count", 0)
        if failing_subjects >= 2:
            contribution = min(35, failing_subjects * 10)
            score += contribution
            factors.append({
                "rule": "multiple_failing_subjects",
                "value": failing_subjects,
                "threshold": 2,
                "weight": 35,
                "contribution": contribution
            })

        # 3. Homework Compliance (Weight: 25)
        homework_missing = student_data.get("homework_missing_count", 0)
        if homework_missing > 5:
            contribution = 25
            score += contribution
            factors.append({
                "rule": "chronic_missing_homework",
                "value": homework_missing,
                "threshold": 5,
                "weight": 25,
                "contribution": contribution
            })

        # Determine level
        level = "low"
        if score >= 60:
            level = "high"
        elif score >= 30:
            level = "medium"

        return {
            "risk_score": score,
            "level": level,
            "factors": factors
        }
