from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.runner import run_compose_service

router = APIRouter(prefix="/dbt", tags=["dbt"])

DBT_COMPOSE_FILE = "/home/mike/dbt/docker-compose.yml"
DBT_SERVICE = "dbt"

_last_run: dict | None = None


def _run(command: list[str], label: str) -> dict:
    global _last_run
    result = run_compose_service(DBT_COMPOSE_FILE, DBT_SERVICE, command)
    _last_run = {**result, "command": label, "ran_at": datetime.now(timezone.utc).isoformat()}
    return result


@router.get("/status")
def dbt_status():
    if _last_run is None:
        return JSONResponse(status_code=503, content={"status": "no_runs_yet"})
    status_code = 200 if _last_run["success"] else 503
    return JSONResponse(status_code=status_code, content=_last_run)


@router.post("/run")
def run_dbt():
    return _run(["run", "--profiles-dir", "."], "run")


@router.post("/seed")
def seed_dbt():
    return _run(["seed", "--full-refresh", "--profiles-dir", "."], "seed")


@router.post("/build")
def build_dbt():
    return _run(["build", "--profiles-dir", "."], "build")


@router.post("/docs")
def generate_docs():
    return _run(["docs", "generate", "--profiles-dir", "."], "docs")
