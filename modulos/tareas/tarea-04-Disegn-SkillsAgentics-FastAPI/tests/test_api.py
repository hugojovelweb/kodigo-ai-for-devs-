from starlette.testclient import TestClient # type: ignore

from app.main import app

client = TestClient(app)


def test_health_check_returns_version() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "1.0.0"


def test_statistics_analysis_returns_expected_counts() -> None:
    response = client.post(
        "/v1/text/analyze",
        json={"text": "FastAPI crea APIs. FastAPI documenta APIs.", "mode": "statistics"},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["word_count"] == 6
    assert body["unique_word_count"] == 4
    assert "fastapi" in body["keywords"]


def test_blank_text_is_rejected_with_structured_error() -> None:
    response = client.post("/v1/text/analyze", json={"text": "   "})
    assert response.status_code == 422
    assert response.json()["error"] == "VALIDATION_ERROR"
