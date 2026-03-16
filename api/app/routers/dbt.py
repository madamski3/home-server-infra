from fastapi import APIRouter
from app.core.runner import run_compose_service

router = APIRouter(prefix="/dbt", tags=["dbt"])

DBT_COMPOSE_FILE = "/home/mike/dbt/docker-compose.yml"
DBT_SERVICE = "dbt"


@router.post("/run")
def run_dbt():
    return run_compose_service(DBT_COMPOSE_FILE, DBT_SERVICE, ["run", "--profiles-dir", "."])


@router.post("/seed")
def seed_dbt():
    return run_compose_service(DBT_COMPOSE_FILE, DBT_SERVICE, ["seed", "--full-refresh", "--profiles-dir", "."])
