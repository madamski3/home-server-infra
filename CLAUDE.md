# Home Server — Claude Context

## Overview
Personal home server used for self-hosted infrastructure, personal projects, and eventually a public-facing portfolio site. All services run in Docker Compose. Only personal/solo use — no multi-tenant or team concerns.

## Access
- SSH: `mike@100.94.165.38` (Tailscale IP, key-only auth)
- OS user: `mike`
- GitHub: https://github.com/madamski3/home-server-infra.git
- Local repo: `/home/mike/infra/`

## Architecture
All services follow the same pattern:
```
/home/mike/infra/<service>/
  docker-compose.yml
  data/               # persistent volume (mounted into container)
  .env                # secrets, not committed to git (symlink to ../.env if no secrets needed)
```

All services are joined to a shared external Docker network called `server-network`. This allows containers to communicate directly by container name (e.g. `postgres-postgres-1`) without going through host ports.

## Services

| Service             | Directory                   | Ports         | Notes                          |
|---------------------|-----------------------------|---------------|--------------------------------|
| nginx-proxy-manager | `/home/mike/infra/nginx-proxy-manager/` | 80, 81 (admin), 443 | Reverse proxy + SSL. Port 81 is the admin UI. |
| postgres            | `/home/mike/infra/postgres/`      | 5432          | No apps connected yet. Data at `./data/`. |
| pgadmin             | (in postgres compose)       | 5050          | Postgres web UI                |
| uptime-kuma         | `/home/mike/uptime-kuma/`   | 3001          | Uptime monitoring              |
| duckdb              | `/home/mike/infra/duckdb/`  | 9999          | Analytical warehouse. HTTP API + web UI via httpserver community extension. Pinned to duckdb==1.4.1 (latest version with httpserver support). No auth — secured by Tailscale binding. |

## Networking Notes
- Accessed via Tailscale only — no public domain configured yet.
- Admin/internal ports (81, 5432, 5050, 3001) are bound to the Tailscale IP (`${TAILSCALE_IP}` from `/home/mike/.env`) — reachable from Tailscale-connected devices only.
- Public ports (80, 443) are bound to all interfaces for nginx-proxy-manager.
- Inter-service communication uses the `server-network` Docker network — containers reference each other by container name, no host ports needed.
- Future plan: point a domain at this server and use nginx-proxy-manager to route traffic + manage SSL.

## Conventions
- New services get their own directory under `/home/mike/infra/` with a `docker-compose.yml`.
- Secrets go in per-service `.env` files (never committed). Shared non-secret vars (e.g. `TAILSCALE_IP`) live in `/home/mike/infra/.env`.
- New app repos (portfolio, personal tools, etc.) live as siblings at `/home/mike/<app-name>/`, each with their own git repo.
- All new services must join `server-network` to participate in inter-service communication.
- Admin/internal ports should be bound to `${TAILSCALE_IP}`, not `0.0.0.0`.
- Postgres will be the standard database for new apps.

## Near-Term Priorities
1. Connect Postgres to the first app.

## Risk Posture
- Downtime of an hour or two is acceptable.
- **Irreversible actions require confirmation** — especially anything touching `data/` directories (these are the persistent Docker volumes and contain state that can't be recovered without a backup).
- No backup system is in place yet — treat all data as non-recoverable for now.
