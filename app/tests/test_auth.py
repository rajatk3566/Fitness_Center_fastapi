import pytest
from app.core.security import get_password_hash

@pytest.mark.auth
class TestAuth:
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            ("testuser1@example.com", "StrongPass123", 201),  
            ("invalid-email", "short", 422), 
            ("", "ValidPass123", 422),  
            ("testuser2@example.com", "", 422), 
            ("validuser@example.com", "12345", 422),  
        ],
    )
    def test_register(self, client, email, password, expected_status):  
        response = client.post(
            "/api/v1/auth/signup", 
            json={"email": email, "password": password}
        )
        assert response.status_code == expected_status

    def test_login_success(self, client, db):
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={"email": "test@example.com", "password": "StrongPass123"}
        )
        assert signup_response.status_code == 201

        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "StrongPass123"}
        )
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

    def test_get_current_user(self, client, db):
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={"email": "test@example.com", "password": "StrongPass123"}
        )
        assert signup_response.status_code == 201

        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "StrongPass123"}
        )
        token = login_response.json()["access_token"]

        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "test@example.com"