import logging

from fastapi import FastAPI

from api.routes.publications import router as publications_router
from core.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="AI Multi-Agent Orchestrator",
    description=(
        "PoC de Legal Tech: análise de publicações judiciais, redação automatizada "
        "de contrarrazões e simulação de protocolo via LangGraph."
    ),
    version="0.1.0",
)

app.include_router(publications_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
