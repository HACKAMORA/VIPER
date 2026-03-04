DeepScan Backend – Network Discovery
===================================

Phase 1 backend for the **DeepScan** pentest automation platform. This service exposes a FastAPI-based REST API that runs network discovery scans (ARP + Nmap), persists results to PostgreSQL via SQLAlchemy, and serves topology/asset data to the VIPER frontend.

## Tech stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x (async, PostgreSQL via asyncpg)
- Alembic (DB migrations)
- Pydantic v2 (+ pydantic-settings)
- python-nmap
- Scapy
- mac-vendor-lookup

## Quickstart

1. Create and configure a Python virtualenv.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

## High-level architecture

- `app/main.py` – FastAPI application, router registration, lifespan hooks.
- `app/config.py` – Typed settings loaded from environment using Pydantic.
- `app/database.py` – Async SQLAlchemy engine + session dependency.
- `app/models` – ORM models for `Scan` and `Host`.
- `app/schemas` – Pydantic schemas for API requests/responses.
- `app/routers/discovery.py` – All `/api/discovery/*` endpoints.
- `app/services/network_scanner.py` – Orchestrates ARP sweep + Nmap scan + classification.
- `app/services/fingerprint.py` – Extracts OS and service metadata from Nmap results.
- `app/utils/ip_utils.py` – CIDR parsing and IP validation helpers.

## Notes

- Scans are executed asynchronously in the background so API calls remain responsive.
- The discovery pipeline is intentionally modular; later phases (fingerprinting, exploitation) can hook into the same `Scan` / `Host` records and extend the data model without breaking existing endpoints.

