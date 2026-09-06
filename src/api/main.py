from fastapi import FastAPI

app = FastAPI(
    title="AI Multi-Agent Orchestrator",
    description="PoC de triagem de tickets de suporte e aprovação corporativa via LangGraph.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
