import pytest
from fastapi import status
from io import BytesIO


class TestAnalyzeExtended:
    def test_analyze_with_valid_jpeg(self, client, auth_headers):
        file_content = b"\xff\xd8\xff\xe0" + b"\x00" * 100
        files = {"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
        
        response = client.post("/api/analyze", files=files, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "id" in data
        assert "filename" in data
        assert data["filename"].endswith(".jpg")

    def test_analyze_with_valid_png(self, client, auth_headers):
        file_content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
        files = {"file": ("test.png", BytesIO(file_content), "image/png")}
        
        response = client.post("/api/analyze", files=files, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_analyze_with_expired_token(self, client, test_user):
        headers = {"Authorization": "Bearer invalid_token_here"}
        files = {"file": ("test.jpg", BytesIO(b"fake"), "image/jpeg")}
        
        response = client.post("/api/analyze", files=files, headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_analyze_without_file(self, client, auth_headers):
        response = client.post("/api/analyze", headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_analyze_with_gif_rejected(self, client, auth_headers):
        files = {"file": ("test.gif", BytesIO(b"GIF89a"), "image/gif")}
        response = client.post("/api/analyze", files=files, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestAuthExtended:
    def test_register_invalid_email(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "notanemail",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_short_password(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "123"
            }
        )
        assert response.status_code == status.HTTP_200_OK

    def test_login_missing_username(self, client):
        response = client.post(
            "/api/auth/login",
            data={"password": "password123"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_missing_password(self, client):
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_empty_credentials(self, client):
        response = client.post(
            "/api/auth/login",
            data={"username": "", "password": ""}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestHealthExtended:
    def test_root_contains_version(self, client):
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "version" in data
        assert "message" in data

    def test_health_contains_status(self, client):
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"


class TestSecurity:
    def test_sql_injection_in_username(self, client):
        response = client.post(
            "/api/auth/login",
            data={"username": "admin' OR '1'='1", "password": "anything"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_xss_in_username_register(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "<script>alert('xss')</script>",
                "email": "xss@example.com",
                "password": "password123"
            }
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_auth_header_format(self, client, auth_headers):
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
