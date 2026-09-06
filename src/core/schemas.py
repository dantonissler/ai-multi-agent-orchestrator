from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class DecisionOutcome(StrEnum):
    FAVORAVEL = "favoravel"
    DESFAVORAVEL = "desfavoravel"
    INDETERMINADO = "indeterminado"


class PublicationInput(BaseModel):
    publication_text: str = Field(
        ..., min_length=1, description="Texto da publicação ou sentença judicial."
    )
    case_number: str = Field(..., description="Número do processo.")
    client_name: str = Field(..., description="Nome do cliente representado.")
    court: str | None = Field(default=None, description="Tribunal ou vara de origem.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    outcome: DecisionOutcome = DecisionOutcome.INDETERMINADO
    confidence: float | None = None
    reasoning: str | None = None


class DraftResult(BaseModel):
    document_type: str = "contrarrazoes"
    content: str | None = None
    is_ready: bool = False


class FilingResult(BaseModel):
    protocol_number: str | None = None
    status: str = "pending"
    filed_at: str | None = None


class OrchestratorState(BaseModel):
    publication: PublicationInput
    analysis: AnalysisResult | None = None
    draft: DraftResult | None = None
    filing: FilingResult | None = None
    current_step: str = "supervisor"
    is_finalized: bool = False


class ProcessPublicationResponse(BaseModel):
    message: str
    state: OrchestratorState
