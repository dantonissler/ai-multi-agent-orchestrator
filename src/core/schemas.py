from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TicketCategory(StrEnum):
    SUPORTE_TECNICO = "suporte_tecnico"
    REEMBOLSO = "reembolso"
    DESCONHECIDO = "desconhecido"


class TicketInput(BaseModel):
    message: str = Field(..., description="Mensagem original do usuário ou ticket.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClassificationResult(BaseModel):
    category: TicketCategory = TicketCategory.DESCONHECIDO
    confidence: float | None = None
    reasoning: str | None = None


class ExtractionResult(BaseModel):
    is_complete: bool = False
    missing_fields: list[str] = Field(default_factory=list)
    extracted_data: dict[str, Any] = Field(default_factory=dict)


class OrchestratorState(BaseModel):
    ticket: TicketInput
    classification: ClassificationResult | None = None
    extraction: ExtractionResult | None = None
    user_prompt: str | None = None
    is_finalized: bool = False
