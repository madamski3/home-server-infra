# Infra Repo — Claude Context

## Access
- GitHub: https://github.com/madamski3/home-server-infra.git
- Local path: `/home/mike/infra/`

## Services in This Repo

| Service             | Directory                   | Notes                          |
|---------------------|-----------------------------|--------------------------------|
| nginx-proxy-manager | `nginx-proxy-manager/`      | Reverse proxy + SSL            |
| postgres            | `postgres/`                 | Shared PostgreSQL + pgadmin    |
| clickhouse          | `clickhouse/`               | Analytical warehouse           |
| api                 | `api/`                      | Internal pipeline API          |
| netdata             | `netdata/`                  | Host system metrics            |

## Manual Setup Steps (one-time, not in docker-compose)

### ClickHouse — required after first `docker compose up`
Run these commands once to create the virtual PostgreSQL source database and the seeds database:
```bash
docker exec -i clickhouse-clickhouse-1 clickhouse-client --password <CLICKHOUSE_PASSWORD> --query "
CREATE DATABASE IF NOT EXISTS raw ENGINE = PostgreSQL('postgres-postgres-1:5432', 'youtube', 'fivetran', '<FIVETRAN_PASSWORD>', 'raw');
CREATE DATABASE IF NOT EXISTS manual;
"
```
- `raw` — virtual ClickHouse database backed by the `raw` schema in the `youtube` PostgreSQL database. Used by dbt as the source catalog.
- `manual` — empty ClickHouse database for dbt seed tables.

Both passwords are in their respective `.env` files (`infra/clickhouse/.env` and `infra/postgres/.env`).

## Near-Term Priorities
1. Connect Postgres to the first app.
