"""Core Attendance Business Logic & Conflict Resolution Engine."""

from typing import Any, Dict, List, Tuple
import datetime

def resolve_offline_batch(
    server_records: dict[str, dict[str, Any]], 
    client_records: list[dict[str, Any]], 
    base_version: int
) -> list[dict[str, Any]]:
    """
    Pure function to resolve record-level optimistic versioning conflicts.
    
    server_records: Dict mapping student_id -> { "status": str, "remarks": str, "record_version": int, "marked_by": str }
    client_records: List of { "student_id": str, "status": str, "remarks": str }
    base_version: The session version the client last saw.
    
    Returns: List of result decisions per student.
    """
    results = []
    
    for op in client_records:
        sid = op["student_id"]
        status = op["status"]
        remarks = op.get("remarks")
        
        server = server_records.get(sid)
        
        # Scenario 1: No server record yet
        if not server:
            results.append({
                "student_id": sid,
                "result": "applied",
                "action": "insert",
                "status": status,
                "remarks": remarks
            })
            continue
            
        # Scenario 2: Identical status and remarks
        if server["status"] == status and server.get("remarks") == remarks:
            results.append({
                "student_id": sid,
                "result": "unchanged",
                "action": "none"
            })
            continue
            
        # Scenario 3: Different, and client had seen the latest version
        if server["record_version"] <= base_version:
            results.append({
                "student_id": sid,
                "result": "applied",
                "action": "update",
                "status": status,
                "remarks": remarks
            })
            continue
            
        # Scenario 4: Different, and client was stale (Conflict)
        results.append({
            "student_id": sid,
            "result": "conflict",
            "action": "none",
            "server_value": {
                "status": server["status"],
                "remarks": server.get("remarks"),
                "marked_by": server.get("marked_by")
            }
        })
        
    return results


class AttendanceEngine:
    """Service handling attendance logic, constraints, and summary generation."""
    
    @staticmethod
    def compute_daily_summary(records: List[Dict[str, Any]], is_submitted: bool) -> Dict[str, Any]:
        """Pure function to compute counts for dashboard fast-reads."""
        summary = {
            "total_students": len(records),
            "present_count": 0,
            "absent_count": 0,
            "late_count": 0,
            "half_day_count": 0,
            "leave_count": 0,
            "excused_count": 0,
            "is_submitted": is_submitted
        }
        
        for record in records:
            status = record["status"]
            if status == "present": summary["present_count"] += 1
            elif status == "absent": summary["absent_count"] += 1
            elif status == "late": summary["late_count"] += 1
            elif status == "half_day": summary["half_day_count"] += 1
            elif status == "leave": summary["leave_count"] += 1
            elif status == "excused": summary["excused_count"] += 1
            
        return summary
    
    @staticmethod
    def calculate_percentage(present_count: int, late_count: int, half_day_count: int, absent_count: int) -> float:
        """Percentage = sum(weights) ÷ (marked days). Excused/Leave excluded from denominator."""
        total_marked = present_count + late_count + half_day_count + absent_count
        if total_marked == 0:
            return 0.0
            
        # Weights: present 1, late 1, half 0.5, absent 0
        score = (present_count * 1.0) + (late_count * 1.0) + (half_day_count * 0.5) + (absent_count * 0.0)
        return round((score / total_marked) * 100, 2)
