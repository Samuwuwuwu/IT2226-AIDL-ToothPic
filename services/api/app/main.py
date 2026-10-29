"""FastAPI entry point. No screening model or LLM is connected yet."""

from fastapi import FastAPI

app = FastAPI(title="AIDL Group 7 API", version="0.1.0")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aidl-api"}
