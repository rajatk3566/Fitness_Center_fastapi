import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.database import get_db
from ..models import User as UserModel
from ..models import Member as MemberModel
from ..api.deps import get_current_active_user


@pytest.fixture
def mock_user():
    return UserModel(id=4, email="test@example.com", is_active=True)


@pytest.fixture
def mock_member(mock_user):
    return MemberModel(
        id=1,
        user_id=mock_user.id,
        membership_status=True,
        membership_start=datetime.now(),
        membership_end=datetime.now() + timedelta(days=30),
        created_at=datetime.now(),
    )


@pytest.fixture
def mock_db(mock_member):
    db = Mock()
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_member
    db.query.return_value = mock_query
    return db


@pytest.fixture
def override_get_db(mock_db):
    def _override_get_db():
        return mock_db

    return _override_get_db


@pytest.fixture
def override_get_current_user(mock_user):
    def _override_get_current_user():
        return mock_user

    return _override_get_current_user


@pytest.fixture
def client_with_auth(client, override_get_db, override_get_current_user):
    client.app.dependency_overrides[get_db] = override_get_db
    client.app.dependency_overrides[get_current_active_user] = override_get_current_user
    yield client
    client.app.dependency_overrides = {}


def test_get_membership_status(client_with_auth):
    response = client_with_auth.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()

    assert "membership_status" in data
    assert "membership_start" in data
    assert "membership_end" in data
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert isinstance(data["membership_status"], bool)
    assert isinstance(data["id"], int)
    assert isinstance(data["user_id"], int)


def test_renew_membership(client_with_auth):
    response = client_with_auth.post("/api/v1/renew")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "new_end_date" in data
    assert data["message"] == "Membership renewed successfully"

    try:
        datetime.fromisoformat(data["new_end_date"])
    except ValueError:
        pytest.fail("new_end_date is not in valid ISO format")


def test_get_membership_history(client_with_auth):
    response = client_with_auth.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    for event in data:
        assert "event_type" in event
        assert "date" in event
        assert "details" in event
        assert event["event_type"] in ["membership_start", "membership_end"]

        try:
            datetime.fromisoformat(event["date"])
        except ValueError:
            pytest.fail(f"Invalid date format in event: {event}")


def test_get_membership_status_not_found(client_with_auth, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client_with_auth.get("/api/v1/")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Membership not found"


def test_renew_membership_not_found(client_with_auth, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client_with_auth.post("/api/v1/renew")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Membership not found"


@pytest.fixture
def sample_member_data():
    return {
        "membership_status": True,
        "membership_start": datetime.now().isoformat(),
        "membership_end": (datetime.now() + timedelta(days=60)).isoformat(),
        "user_id": 4,
    }
