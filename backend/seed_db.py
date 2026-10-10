import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.tenant import School
from app.models.identity import User
from app.core.security import get_password_hash

# You can adjust this to your actual DB URL
DATABASE_URL = "postgresql+asyncpg://erp_owner:supersecretpassword@localhost:5432/educore_erp"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def seed():
    async with async_session_maker() as session:
        # 1. Ensure DEMO school exists
        stmt = select(School).where(School.code == "DEMO")
        result = await session.execute(stmt)
        school = result.scalars().first()

        if not school:
            school = School(
                name="Demo International School",
                code="DEMO",
                status="active"
            )
            session.add(school)
            await session.commit()
            await session.refresh(school)
            print(f"Created School: {school.name}")

        # 2. Check if Hari exists
        stmt_user = select(User).where(User.email == "hari@student.com")
        result_user = await session.execute(stmt_user)
        hari = result_user.scalars().first()

        if not hari:
            # Create Hari
            hashed_password = get_password_hash("hari@2006")
            hari = User(
                school_id=school.id,
                email="hari@student.com",
                full_name="Hari Student",
                password_hash=hashed_password,
                status="active"
            )
            session.add(hari)
            await session.commit()
            print("Successfully created student: hari@student.com with password: hari@2006")
        else:
            # Update password just in case
            hari.password_hash = get_password_hash("hari@2006")
            await session.commit()
            print("Updated existing student: hari@student.com with password: hari@2006")

if __name__ == "__main__":
    asyncio.run(seed())
