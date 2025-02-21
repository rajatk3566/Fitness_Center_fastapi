import pytest
from app.core.security import get_password_hash

@pytest.mark.auth
class TestAuth:
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            ("testuser1@example.com", "StrongPass123", 201),  # Valid case
            ("invalid-email", "short", 422),  # Invalid email format
            ("", "ValidPass123", 422),  # Empty email
            ("testuser2@example.com", "", 422),  # Empty password
            ("validuser@example.com", "12345", 422),  # Short password
            ("test.user@example.com", "StrongPass123!", 201),  # Email with dots
            ("TEST@EXAMPLE.COM", "StrongPass123", 201),  # Uppercase email
            ("existing@example.com", "StrongPass123", 400),  # Duplicate email
            ("testuser3@example.com", " ", 422),  # Whitespace password
        ],
    )
    def test_register(self, client, email, password, expected_status):
        # Pre-create user for duplicate email test
        if email == "existing@example.com":
            first_response = client.post(
                "/api/v1/auth/signup",
                json={"email": email, "password": "StrongPass123"}
            )
            assert first_response.status_code == 201
    
        response = client.post(
            "/api/v1/auth/signup",
            json={"email": email, "password": password}
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "login_data, expected_status",
        [
            ({"username": "test@example.com", "password": "StrongPass123"}, 200),  # Valid login
            ({"username": "test@example.com", "password": "WrongPass123"}, 401),  # Wrong password
            ({"username": "nonexistent@example.com", "password": "StrongPass123"}, 401),  # Non-existent user
            ({"username": "test@example.com", "password": ""}, 401),  # Empty password returns 401
            ({"username": "", "password": "StrongPass123"}, 401),  # Empty username returns 401
        ]
    )
    def test_login_scenarios(self, client, db, login_data, expected_status):
        # Create test user if we're testing with the test@example.com account
        if login_data["username"] == "test@example.com" and login_data["password"] != "":
            signup_response = client.post(
                "/api/v1/auth/signup",
                json={"email": "test@example.com", "password": "StrongPass123"}
            )
            assert signup_response.status_code == 201

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == expected_status
        if expected_status == 200:
            assert "access_token" in response.json()
            assert response.json()["token_type"] == "bearer"

    def test_get_current_user(self, client, db):
        # Create and login user
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
        token = login_response.json()["access_token"]

        # Test valid token
        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "test@example.com"

        # Test invalid token
        invalid_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert invalid_response.status_code == 401

        # Test missing token
        no_token_response = client.get("/api/v1/auth/me")
        assert no_token_response.status_code == 401