"""Development data seeder. DO NOT RUN IN PRODUCTION."""

import logging
import argparse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.tenant import School
from app.models.academic import AcademicYear
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed(perf: bool = False):
    db: Session = SessionLocal()
    try:
        # Create a test school if none exists
        school = db.query(School).first()
        if not school:
            school = School(name="Demo High School", code="DEMO01", timezone="Asia/Kolkata")
            db.add(school)
            db.flush()
            logger.info(f"Created school {school.code}")
            
        # Create current academic year
        year = db.query(AcademicYear).filter_by(school_id=school.id, status="active").first()
        if not year:
            year = AcademicYear(
                school_id=school.id, 
                name="2026-2027", 
                start_date=datetime.date(2026, 6, 1), 
                end_date=datetime.date(2027, 4, 30),
                status="active"
            )
            db.add(year)
            db.flush()
            logger.info(f"Created academic year {year.name}")

        db.commit()
        logger.info("Basic seed completed.")
        
        if perf:
            logger.info("Perf flag passed. (Placeholder for 1,500 students & 40 sections seeding)")
            # Phase 4 prompt requests generating 1500 students here.

    except Exception as e:
        db.rollback()
        logger.error(f"Seed failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--perf", action="store_true", help="Generate volume data for k6 testing")
    args = parser.parse_args()
    seed(args.perf)
