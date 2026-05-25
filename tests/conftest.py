from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

from app.dependency import get_db
from main import app
from app.database import Base
from app.models import User, Wallet


TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

@pytest.fixture()
def client():
    yield TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    #Пересоздание таблицы перед тестом
    Base.metadata.create_all(bind=test_engine)
    yield 
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()    

@pytest.fixture()
def test_user(db_session) -> User:
    user = User(login="test")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture()
def test_wallet(db_session, test_user) -> Wallet:
    wallet = Wallet(name="card", balance=200, user_id=test_user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)
    return wallet
    
@pytest.fixture
def auth_headers(test_user) -> dict:
    """Возвращает заголовки авторизации"""
    return {"Authorization": f"Bearer {test_user.login}"}