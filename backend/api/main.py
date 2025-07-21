from fastapi import FastAPI
from backend.api.routes import query

app = FastAPI(title="RegRAG API")

app.include_router(
    query.router,
    prefix="/api/v1",
)
