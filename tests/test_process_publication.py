from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from core.config import Settings

client = TestClient(app)

SAMPLE_TEXT = "SENTENÇA: Ante o exposto, JULGO IMPROCEDENTE o pedido formulado pelo autor."


def test_process_publication_rejects_empty_text() -> None:
    response = client.post("/api/v1/process-publication", json={"text": ""})
    assert response.status_code == 422


def test_missing_api_key_returns_503() -> None:
    settings = Settings(openai_api_key=None)
    with patch("api.routes.get_settings", return_value=settings):
        response = client.post("/api/v1/process-publication", json={"text": SAMPLE_TEXT})
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_process_publication_favorable_skips_draft() -> None:
    mock_result = {
        "publication_text": SAMPLE_TEXT,
        "is_favorable": True,
        "analysis_reason": "Decisão favorável ao cliente.",
    }
    settings = Settings(openai_api_key="test-key")
    with (
        patch("api.routes.get_settings", return_value=settings),
        patch("api.routes.legal_workflow.invoke", return_value=mock_result),
    ):
        response = client.post("/api/v1/process-publication", json={"text": SAMPLE_TEXT})
    assert response.status_code == 200
    data = response.json()
    assert data["is_favorable"] is True
    assert "drafted_appeal" not in data
    assert "protocol_receipt" not in data


def test_process_publication_unfavorable_full_flow() -> None:
    mock_result = {
        "publication_text": SAMPLE_TEXT,
        "is_favorable": False,
        "analysis_reason": "Sentença de improcedência desfavorável ao cliente.",
        "drafted_appeal": "CONTRARRAZÕES: ...",
        "protocol_receipt": (
            "Protocolo abc-123 registrado com sucesso via API simulada do tribunal."
        ),
    }
    settings = Settings(openai_api_key="test-key")
    with (
        patch("api.routes.get_settings", return_value=settings),
        patch("api.routes.legal_workflow.invoke", return_value=mock_result),
    ):
        response = client.post("/api/v1/process-publication", json={"text": SAMPLE_TEXT})
    assert response.status_code == 200
    data = response.json()
    assert data["is_favorable"] is False
    assert data["drafted_appeal"] == "CONTRARRAZÕES: ..."
    assert "Protocolo abc-123" in data["protocol_receipt"]
