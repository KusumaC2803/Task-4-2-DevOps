import argparse
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def run_check(url, total_requests, workers):
    latencies = []
    failures = 0

    def one_request():
        started = time.perf_counter()
        try:
            response = requests.get(url, timeout=5)
            elapsed_ms = (time.perf_counter() - started) * 1000
            return response.ok, elapsed_ms
        except requests.RequestException:
            elapsed_ms = (time.perf_counter() - started) * 1000
            return False, elapsed_ms

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one_request) for _ in range(total_requests)]
        for future in as_completed(futures):
            ok, elapsed_ms = future.result()
            latencies.append(elapsed_ms)
            if not ok:
                failures += 1

    ordered = sorted(latencies)
    p95_index = max(0, min(len(ordered) - 1, int(len(ordered) * 0.95) - 1))
    p95 = ordered[p95_index]

    return {
        "requests": total_requests,
        "workers": workers,
        "successes": total_requests - failures,
        "failures": failures,
        "min_ms": min(latencies),
        "avg_ms": statistics.mean(latencies),
        "p95_ms": p95,
        "max_ms": max(latencies),
    }


def main():
    parser = argparse.ArgumentParser(description="Simple Task 4 load-readiness check")
    parser.add_argument("--url", default="http://127.0.0.1:8000/health")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--target-p95-ms", type=float, default=200)
    args = parser.parse_args()

    result = run_check(args.url, args.requests, args.workers)

    print(f"requests={result['requests']} workers={result['workers']}")
    print(f"successes={result['successes']}")
    print(f"failures={result['failures']}")
    print(f"min_ms={result['min_ms']:.2f}")
    print(f"avg_ms={result['avg_ms']:.2f}")
    print(f"p95_ms={result['p95_ms']:.2f}")
    print(f"max_ms={result['max_ms']:.2f}")
    print(f"target_p95_ms={args.target_p95_ms:.0f}")

    passed = result["failures"] == 0 and result["p95_ms"] <= args.target_p95_ms
    print("RESULT=PASS" if passed else "RESULT=FAIL")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
