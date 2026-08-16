# Task 4 Runbook — Load Readiness

## 1. Start

Create a clean Python environment and install the requirements.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 2. Verify

Check the health endpoint:

```text
GET /health
```

Expected response:

```json
{"status":"ok","service":"applications-shortlisting"}
```

## 3. Functional journey

1. A student applies to a job using `POST /applications`.
2. The application records whether the student meets the required skill threshold.
3. A company views applications using `GET /companies/applications`.
4. An eligible candidate can be shortlisted using `POST /companies/shortlist`.
5. A candidate below the threshold is rejected from shortlisting with a clear error.

## 4. Load check

Run:

```bash
python scripts/load_check.py --requests 100 --workers 10 --target-p95-ms 200
```

The important evidence is zero failures and p95 below the target.

The test uses real HTTP requests against the running service rather than only calling Python functions.

## 5. Failure handling

- Unknown student -> HTTP 404.
- Unknown job -> HTTP 404.
- Unknown application -> HTTP 404.
- Candidate below required skills -> HTTP 400.
- Service unavailable during load check -> failed requests are counted.

## 6. Rollback / recovery

For this local demo:
1. Stop the running server with `Ctrl+C`.
2. Return to the last known-good Git commit.
3. Reinstall requirements if dependencies changed.
4. Start the API again.
5. Run `pytest -q`.
6. Run the load check again.
7. Only treat the version as ready after the checks pass.

For a cloud deployment, the same idea should be implemented through the CI/CD pipeline with a previous image/version available for rollback.

## 7. Secrets

No credentials are stored in the repository. Production secrets should be injected through environment configuration or a managed secrets service.

## 8. Monitoring evidence

For this student-sized task, the load-check output is the primary evidence. In a production deployment, this should be extended with application logs, request rate, error rate, latency and alerting.
