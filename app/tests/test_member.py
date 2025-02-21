import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import User
from app.core.security import get_password_hash

@pytest.mark.member
class TestMember:
    @pytest.fixture
    def admin_user(self, db: Session):
        admin_email = "admin@example.com"
        admin_password = "StrongPass123"
        
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash(admin_password),
                is_active=True,
                is_admin=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            
        return {"email": admin_email, "password": admin_password}

    @pytest.fixture
    def auth_headers(self, client, admin_user):
        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": admin_user["email"], "password": admin_user["password"]}
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def user_id(self, client, auth_headers):
        me_response = client.get("/api/v1/auth/me", headers=auth_headers)
        return me_response.json()["id"]

    @pytest.fixture
    def sample_member_data(self, user_id):
        return {
            "membership_status": True,
            "membership_start": datetime.now().isoformat(),
            "membership_end": (datetime.now() + timedelta(days=365)).isoformat(),
            "user_id": user_id
        }

    def test_create_member(self, client, auth_headers, sample_member_data):
        response = client.post(
            "/api/v1/members/",
            json=sample_member_data,
            headers=auth_headers
        )
        
        print(f"Create member response: {response.status_code}")
        print(f"Response body: {response.text}")
        
        assert response.status_code == 201
        data = response.json()
        assert data["membership_status"] == sample_member_data["membership_status"]
        assert "id" in data
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_all_members(self, client, auth_headers, sample_member_data):
        create_response = client.post(
            "/api/v1/members/",
            json=sample_member_data,
            headers=auth_headers
        )
        assert create_response.status_code == 201
        
        response = client.get("/api/v1/members/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        member = data[0]
        assert all(key in member for key in [
            "id", "user_id", "membership_status", 
            "membership_start", "membership_end",
            "created_at", "updated_at"
        ])

    def test_delete_member(self, client, auth_headers, sample_member_data):
        # Create a member first
        create_response = client.post(
            "/api/v1/members/",
            json=sample_member_data,
            headers=auth_headers
        )
        assert create_response.status_code == 201
        member_id = create_response.json()["id"]
        
        response = client.delete(f"/api/v1/members/{member_id}", headers=auth_headers)
        assert response.status_code == 204

