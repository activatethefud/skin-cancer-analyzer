import pytest
from fastapi import status
from io import BytesIO


class TestAnalyze:
    def test_analyze_requires_auth(self, client):
        response = client.post("/api/analyze")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_analyze_history_requires_auth(self, client):
        response = client.get("/api/analyze/history")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_analyze_history_empty(self, client, auth_headers):
        response = client.get("/api/analyze/history", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["analyses"] == []

    def test_analyze_with_mocked_prediction(self, client, auth_headers):
        file_content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
        files = {"file": ("test.png", BytesIO(file_content), "image/png")}
        
        response = client.post("/api/analyze", files=files, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "top_prediction" in data
        assert "confidence" in data
        assert "all_predictions" in data
        assert len(data["all_predictions"]) == 7
        assert data["all_predictions"][0]["class_name"] == "nv"

    def test_analyze_invalid_file_type(self, client, auth_headers):
        files = {"file": ("test.txt", BytesIO(b"hello"), "text/plain")}
        response = client.post("/api/analyze", files=files, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not allowed" in response.json()["detail"].lower()

    def test_analyze_file_too_large(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr("app.routers.analyze.settings.MAX_FILE_SIZE", 100)
        
        file_content = b"\x00" * 200
        files = {"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
        
        response = client.post("/api/analyze", files=files, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "too large" in response.json()["detail"].lower()

    def test_model_status_endpoint(self, client):
        response = client.get("/api/analyze/model-status")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "model_loaded" in data
        assert "message" in data
        assert data["model_loaded"] is False
