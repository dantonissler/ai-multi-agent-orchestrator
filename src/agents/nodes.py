import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from core.config import get_settings
from core.state import LegalState

logger = logging.getLogger(__name__)


class AnalysisOutput(BaseModel):
    is_favorable: bool = Field(description="True se a decisão for favorável ao cliente.")
    analysis_reason: str = Field(description="Justificativa objetiva da análise.")


def _get_llm() -> ChatOpenAI:
    settings = get_settings()
    if not settings.openai_api_key:
        msg = "OPENAI_API_KEY não configurada."
        raise ValueError(msg)
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )


def analyzer_node(state: LegalState) -> dict:
    llm = _get_llm().with_structured_output(AnalysisOutput)
    messages = [
        SystemMessage(
            content=(
                "Você é um analisador jurídico. Leia a publicação judicial e determine "
                "se a decisão é favorável ou desfavorável ao cliente representado. "
                "Responda apenas com o formato estruturado solicitado."
            )
        ),
        HumanMessage(content=state["publication_text"]),
    ]
    result: AnalysisOutput = llm.invoke(messages)
    logger.info("flow.step analyzer -> is_favorable=%s", result.is_favorable)
    return {
        "is_favorable": result.is_favorable,
        "analysis_reason": result.analysis_reason,
    }


def drafter_node(state: LegalState) -> dict:
    llm = _get_llm()
    messages = [
        SystemMessage(
            content=(
                "Você é um advogado redator. Elabore uma contrarrazão ou recurso "
                "com base na publicação e na análise fornecidas. "
                "Este é um exercício de PoC — produza texto jurídico modelar, "
                "sem alegar validade processual real."
            )
        ),
        HumanMessage(
            content=(
                f"Publicação:\n{state['publication_text']}\n\n"
                f"Análise:\n{state.get('analysis_reason', '')}"
            )
        ),
    ]
    response = llm.invoke(messages)
    drafted_appeal = str(response.content)
    logger.info("flow.step drafter -> appeal_generated")
    return {"drafted_appeal": drafted_appeal}


def filer_node(state: LegalState) -> dict:
    from uuid import uuid4

    protocol_id = str(uuid4())
    protocol_receipt = (
        f"Protocolo {protocol_id} registrado com sucesso via API simulada do tribunal."
    )
    logger.info("flow.step filer -> protocol_receipt=%s", protocol_id)
    return {"protocol_receipt": protocol_receipt}
