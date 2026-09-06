from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

SAMPLE_PAYLOAD = {
    "publication_text": (
        "SENTENÇA: Ante o exposto, JULGO IMPROCEDENTE o pedido formulado pelo autor."
    ),
    "case_number": "0001234-56.2024.8.26.0100",
    "client_name": "Empresa XYZ Ltda",
    "court": "TJSP",
}


def test_process_publication_returns_200_with_stub_response() -> None:
    response = client.post("/api/v1/publications/process", json=SAMPLE_PAYLOAD)
    assert response.status_code == 200

    data = response.json()
    assert "PoC stub" in data["message"]
    assert data["state"]["current_step"] == "finalized"
    assert data["state"]["is_finalized"] is True
    assert data["state"]["analysis"]["outcome"] == "desfavoravel"
    assert data["state"]["filing"]["status"] == "simulated"
    assert data["state"]["filing"]["protocol_number"] == "SIM-000000-POC"


def test_process_publication_rejects_empty_text() -> None:
    payload = {**SAMPLE_PAYLOAD, "publication_text": ""}
    response = client.post("/api/v1/publications/process", json=payload)
    assert response.status_code == 422
