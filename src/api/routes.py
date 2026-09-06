import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.config import get_settings
from core.graph import legal_workflow
from core.state import LegalState

logger = logging.getLogger(__name__)

router = APIRouter(tags=["publications"])


class ProcessPublicationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto da publicação judicial.")


@router.post("/api/v1/process-publication")
def process_publication(body: ProcessPublicationRequest) -> LegalState:
    settings = get_settings()
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail=(
                "OPENAI_API_KEY não configurada. "
                "Copie .env.example para .env e preencha a chave."
            ),
        )

    logger.info("publication.received length=%d", len(body.text))
    result: LegalState = legal_workflow.invoke({"publication_text": body.text})
    logger.info(
        "publication.completed is_favorable=%s protocol=%s",
        result.get("is_favorable"),
        result.get("protocol_receipt"),
    )
    return result
