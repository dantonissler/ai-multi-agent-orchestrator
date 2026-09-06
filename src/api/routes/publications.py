import logging
from datetime import UTC, datetime

from fastapi import APIRouter

from core.schemas import (
    AnalysisResult,
    DecisionOutcome,
    DraftResult,
    FilingResult,
    OrchestratorState,
    ProcessPublicationResponse,
    PublicationInput,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/publications", tags=["publications"])


def _run_stub_flow(publication: PublicationInput) -> OrchestratorState:
    """Simula o fluxo do grafo emitindo logs por etapa (stub)."""
    logger.info(
        "publication.received case_number=%s client=%s",
        publication.case_number,
        publication.client_name,
    )

    state = OrchestratorState(publication=publication, current_step="supervisor")

    logger.info("flow.step supervisor -> analyzer (stub)")
    state.current_step = "analyzer"

    analysis = AnalysisResult(
        outcome=DecisionOutcome.DESFAVORAVEL,
        confidence=None,
        reasoning="Stub: análise será implementada com LLM na próxima etapa.",
    )
    state.analysis = analysis
    logger.info("flow.step analyzer -> outcome=%s (stub)", analysis.outcome)

    if analysis.outcome == DecisionOutcome.FAVORAVEL:
        state.current_step = "finalized"
        state.is_finalized = True
        logger.info("flow.step outcome=favoravel -> fim sem acao (stub)")
        return state

    logger.info("flow.step analyzer -> drafter (stub)")
    state.current_step = "drafter"
    state.draft = DraftResult(
        document_type="contrarrazoes",
        content=None,
        is_ready=False,
    )
    logger.info("flow.step drafter -> document_ready=%s (stub)", state.draft.is_ready)

    logger.info("flow.step drafter -> filer (stub)")
    state.current_step = "filer"
    state.filing = FilingResult(
        protocol_number="SIM-000000-POC",
        status="simulated",
        filed_at=datetime.now(UTC).isoformat(),
    )
    logger.info("flow.step filer -> status=%s (stub)", state.filing.status)

    state.current_step = "finalized"
    state.is_finalized = True
    logger.info("flow.step finalized case_number=%s", publication.case_number)

    return state


@router.post("/process", response_model=ProcessPublicationResponse)
def process_publication(publication: PublicationInput) -> ProcessPublicationResponse:
    """Processa uma publicação judicial pelo fluxo de orquestração (stub)."""
    state = _run_stub_flow(publication)
    return ProcessPublicationResponse(
        message="PoC stub — LangGraph será implementado na próxima etapa.",
        state=state,
    )
