from fastapi import APIRouter, FastAPI
from app.routers import dbt

app = FastAPI(
    title="Server API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

api_router = APIRouter(prefix="/api")
api_router.include_router(dbt.router)


@api_router.get("/health")
def health():
    return {"status": "ok"}


app.include_router(api_router)
