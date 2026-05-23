from __future__ import annotations

import os
import statistics
import time

import httpx


def profile_mode(client: httpx.Client, base_url: str, mode: str) -> list[float]:
    samples: list[float] = []
    for _ in range(5):
        start = time.perf_counter()
        response = client.get(f'{base_url}/api/lab', params={'mode': mode, 'locale': 'es'})
        response.raise_for_status()
        samples.append((time.perf_counter() - start) * 1000)
    return samples


def main() -> int:
    base_url = os.getenv('API_BASE_URL', 'http://localhost:8000').rstrip('/')

    with httpx.Client(timeout=10.0) as client:
        cached = profile_mode(client, base_url, 'cached')
        nocache = profile_mode(client, base_url, 'nocache')

    cached_avg = statistics.mean(cached)
    nocache_avg = statistics.mean(nocache)

    assert cached_avg < nocache_avg, (cached, nocache)

    print('PYTHON profile_cache OK')
    print(f'cached avg={cached_avg:.2f} ms')
    print(f'nocache avg={nocache_avg:.2f} ms')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
