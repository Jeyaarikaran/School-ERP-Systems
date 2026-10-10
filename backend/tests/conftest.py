import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from pydantic import SecretStr

from app.main import app
from app.core.config import settings
from app.core.database import get_db_session
from app.core.security import create_access_token

# Override JWT settings for tests to use HS256 and a simple symmetric key
# This allows us to use the real JWT dependency without needing RSA keys configured
settings.jwt_algorithm = "HS256"
settings.jwt_private_key = SecretStr("test_secret_key_for_jwt_auth_12345")
settings.jwt_public_key = "test_secret_key_for_jwt_auth_12345"

# Test Database Connection (can be overridden via ENV, else uses rollback strategy on main DB)
engine = create_async_engine(settings.database_url, echo=False)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a transactional database session that rolls back after every test."""
    connection = await engine.connect()
    transaction = await connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provides a FastAPI test client with database dependency override."""
    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()

def generate_real_token(school_id: str, role: str = "super_admin") -> str:
    """Helper to generate REAL JWT tokens using the application's actual auth flow."""
    payload = {
        "sub": str(uuid.uuid4()),
        "sid": str(uuid.uuid4()), # Dummy session ID to pass DB revocation check (returns None -> passes)
        "roles": [role],
        "permissions": [
            "student.create", "student.view", "student.update",
            "parent.view", "parent.create",
            "academic_year.create", "academic_year.view",
            "branch.create", "branch.view",
            "school.view", "class.create", "class.view"
        ],
        "school_id": school_id,
    }
    return create_access_token(payload)

@pytest.fixture
def school_a_id():
    return str(uuid.uuid4())

@pytest.fixture
def school_b_id():
    return str(uuid.uuid4())

@pytest.fixture
def school_a_token(school_a_id):
    return generate_real_token(school_a_id, role="super_admin")

@pytest.fixture
def school_b_token(school_b_id):
    return generate_real_token(school_b_id, role="super_admin")

@pytest.fixture
def school_admin_token(school_a_id):
    return generate_real_token(school_a_id, role="school_admin")

@pytest.fixture
def parent_b_id():
    return str(uuid.uuid4())

@pytest.fixture
def parent_a_token(school_a_id):
    return generate_real_token(school_a_id, role="parent")
