"""Curriculum Tracking Core Services."""

from datetime import date
from typing import Dict, Any, List

class CurriculumEngine:
    
    @staticmethod
    def derive_status(status: str, planned_end: date | None, today: date) -> str:
        """
        Pure function to derive 'delayed' status.
        Delayed is true if status != completed and planned_end is in the past.
        """
        if status == "completed":
            return status
            
        if planned_end and planned_end < today:
            return "delayed"
            
        return status
        
    @staticmethod
    def calculate_completion_percentage(units: List[Dict[str, Any]]) -> float:
        """
        Calculates completion percentage based on planned_periods.
        If planned_periods are missing, equal weights (1.0) are assumed.
        """
        if not units:
            return 0.0
            
        total_weight = 0.0
        completed_weight = 0.0
        
        for u in units:
            weight = float(u.get("planned_periods", 1.0))
            if weight == 0:
                weight = 1.0 # fallback for 0-period units
                
            total_weight += weight
            if u.get("status") == "completed":
                completed_weight += weight
                
        if total_weight == 0:
            return 0.0
            
        return round((completed_weight / total_weight) * 100, 2)
