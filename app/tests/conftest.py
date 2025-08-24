import sys
from unittest.mock import MagicMock

sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_community.vectorstores'] = MagicMock()
sys.modules['tiktoken'] = MagicMock()

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.core.config import settings  # noqa: E402

settings.database_url = "sqlite:///:memory:"

from app.main import app  # noqa: E402
from app.db.models import Base  # noqa: E402
from app.db.base import get_db  # noqa: E402
from sqlalchemy import create_engine, StaticPool  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
Base.metadata.create_all(engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db  # type: ignore
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()  # type: ignore
