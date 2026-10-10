import pytest
from app.insights.scorer import RiskScorer

@pytest.mark.unit
def test_risk_scorer_low_risk():
    student_data = {
        "attendance_percentage": 95.0,
        "failing_subjects_count": 0,
        "homework_missing_count": 1
    }
    result = RiskScorer.evaluate(student_data)
    assert result["level"] == "low"
    assert result["risk_score"] == 0
    assert len(result["factors"]) == 0

@pytest.mark.unit
def test_risk_scorer_medium_risk_attendance():
    student_data = {
        "attendance_percentage": 70.0,
        "failing_subjects_count": 0,
        "homework_missing_count": 0
    }
    result = RiskScorer.evaluate(student_data)
    assert result["level"] == "medium"
    assert result["risk_score"] == 40
    assert len(result["factors"]) == 1
    assert result["factors"][0]["rule"] == "attendance_below_threshold"

@pytest.mark.unit
def test_risk_scorer_high_risk_multiple_factors():
    student_data = {
        "attendance_percentage": 65.0,  # +40
        "failing_subjects_count": 3,     # +30
        "homework_missing_count": 10     # +25
    }
    result = RiskScorer.evaluate(student_data)
    assert result["level"] == "high"
    assert result["risk_score"] == 95  # 40 + 30 + 25
    assert len(result["factors"]) == 3

@pytest.mark.unit
def test_finance_is_excluded_from_risk():
    """Ensure financial constraints (like unpaid fees) do not bias risk score."""
    student_data = {
        "attendance_percentage": 100.0,
        "failing_subjects_count": 0,
        "homework_missing_count": 0,
        "unpaid_fees": 50000  # Should be ignored
    }
    result = RiskScorer.evaluate(student_data)
    assert result["level"] == "low"
    assert result["risk_score"] == 0
