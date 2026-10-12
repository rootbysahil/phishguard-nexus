# ADR-001: SQLite over PostgreSQL

**Status:** Accepted  
**Phase:** Phase 0 — Architecture  
**Deciders:** Engineering team

---

## Context

The application needs a relational database to store scan history, feature snapshots, and
aggregated stats. Two realistic options for a self-hosted portfolio project are SQLite and
PostgreSQL.

## Decision

Use **SQLite** as the primary database, accessed via SQLAlchemy ORM.

## Rationale

| Criterion | SQLite | PostgreSQL |
|---|---|---|
| Operational complexity | Zero — file on disk | Requires a running server process |
| Docker compose | One service | Two services + health check dependency |
| Expected write concurrency | Low (single user, < 100 scans/day) | Not a bottleneck |
| Portability | Single file; easy to back up and inspect | Requires dump/restore |
| Reviewer reproducibility | `docker compose up` just works | Reviewer must wait for PG init |
| Upgrade path | SQLAlchemy ORM abstracts the DB | — |

For a single-user local deployment with expected scan volumes below 1,000 per day,
SQLite has no meaningful performance disadvantage. The SQLAlchemy abstraction layer means
migrating to PostgreSQL in the future requires changing only the `DATABASE_URL` env var
and running `alembic upgrade head`.

## Consequences

- Scan writes serialize naturally; no need for connection pooling.
- `DATABASE_URL` in `.env.example` defaults to `sqlite:///./phishguard.db`.
- A comment in `db/session.py` notes the PostgreSQL upgrade path.
- CI uses SQLite; no database service required in GitHub Actions.

## Rejected Alternatives

**PostgreSQL:** Correct for a multi-user production deployment. Rejected here because the
added operational complexity is not justified for a portfolio project and harms
reviewer reproducibility.

**MongoDB:** Document store is a poor fit for structured relational scan data. Rejected.
