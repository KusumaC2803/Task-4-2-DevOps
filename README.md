# Task 4 — Applications & Shortlisting (DevOps)

## Load Readiness

This task adds a small, repeatable load-readiness check around the application/shortlisting flow.

### What is included
- A lightweight FastAPI demo service for student applications and company shortlisting.
- In-memory sample data so the project runs without a database dependency.
- Health endpoint for basic readiness verification.
- Concurrent load-check script using Python threads.
- Configurable request count, workers and target p95 latency.
- Basic automated tests.
- A simple runbook documenting build, test, load-check and rollback steps.

### Why this is DevOps-focused
The goal is not to build a large marketplace. The goal is to show that the service can be started consistently, tested, exercised under concurrent requests, measured with real numbers, and recovered/restarted using a documented process.

## Project flow

Student -> Apply to Job -> Application stored -> Company views applications -> Shortlist candidate

## Quick start

```bash
python -m venv venv
# Windows
venv\Scripts\activate

pip install -r requirements.txt
pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
python scripts/load_check.py
```

Example configurable run:

```bash
python scripts/load_check.py --requests 100 --workers 10 --target-p95-ms 200
```

## Evidence

The load checker prints:
- total requests
- successful/failed requests
- minimum latency
- average latency
- p95 latency
- maximum latency
- configured p95 target
- PASS/FAIL

This gives a simple live number that can be shown during evaluation.

## Security note

No passwords, API keys or cloud credentials are included in this repository. Runtime configuration belongs in environment variables or a secrets manager.

## Rollback

For this demo, rollback means stopping the current process and starting the last known-good project version. The exact steps are in `docs/RUNBOOK.md`.
