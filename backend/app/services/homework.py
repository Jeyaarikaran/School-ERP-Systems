"""Homework Core Services."""

from datetime import datetime
from typing import Dict, Any

class HomeworkEngine:
    
    @staticmethod
    def determine_lateness(due_at: datetime, submitted_at: datetime, allow_late: bool, late_cutoff_at: datetime | None) -> Dict[str, Any]:
        """
        Pure function to evaluate lateness and cutoff rejections strictly from server time.
        """
        is_late = submitted_at > due_at
        
        if is_late:
            if not allow_late:
                return {"allowed": False, "code": "SUBMISSION_CLOSED", "is_late": True}
                
            if late_cutoff_at and submitted_at > late_cutoff_at:
                return {"allowed": False, "code": "LATE_CUTOFF_EXCEEDED", "is_late": True}
                
        return {"allowed": True, "code": None, "is_late": is_late}
        
    @staticmethod
    def validate_marks(marks: float, max_marks: float | None) -> bool:
        """Validates that marks fit within the assigned range."""
        if max_marks is None:
            return True # Ungraded
            
        return 0 <= marks <= max_marks
