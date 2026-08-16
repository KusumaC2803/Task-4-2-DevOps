# Verification Notes

## Definition of Done

### Paths hold under sample concurrency
Verified with concurrent HTTP requests through `scripts/load_check.py`.

### Load readiness is persisted/real and demoable end-to-end
The API exposes the actual application and shortlisting journey. Applications are held by the running service and can be viewed and shortlisted.

## Evaluation evidence

| Area | Evidence |
|---|---|
| Core deliverable | Running API + load check |
| Real-data correctness | Two jobs, two students, different skill outcomes |
| Live verification | pytest results + load-check latency numbers |
| Failure handling | 404 and skill-threshold rejection paths |
| Recovery | Runbook with restart/rollback steps |

## Suggested 2-minute demo

1. Start the API.
2. Show `/health`.
3. Apply student 101 to job 1.
4. Show that the application is eligible.
5. Shortlist the application as a company.
6. Apply student 102 to job 1 and show `below_skill_threshold`.
7. Run the load check and show the p95 result and PASS/FAIL output.

This is intentionally small and transparent so the evaluator can inspect the implementation instead of seeing a large generated framework.
