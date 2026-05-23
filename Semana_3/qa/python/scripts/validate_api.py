from __future__ import annotations

import os

import httpx


def main() -> int:
    base_url = os.getenv('API_BASE_URL', 'http://localhost:8000').rstrip('/')

    with httpx.Client(timeout=10.0) as client:
        health = client.get(f'{base_url}/api/health')
        health.raise_for_status()

        cached = client.get(f'{base_url}/api/lab', params={'mode': 'cached', 'locale': 'es'})
        cached.raise_for_status()

        nocache = client.get(f'{base_url}/api/lab', params={'mode': 'nocache', 'locale': 'es'})
        nocache.raise_for_status()

    health_payload = health.json()
    cached_payload = cached.json()
    nocache_payload = nocache.json()

    assert health_payload['status'] == 'UP', health_payload
    assert cached_payload['performance']['ttfbMs'] < nocache_payload['performance']['ttfbMs'], (
        cached_payload,
        nocache_payload,
    )

    print('PYTHON validate_api OK')
    print(f"cached ttfb={cached_payload['performance']['ttfbMs']} ms")
    print(f"nocache ttfb={nocache_payload['performance']['ttfbMs']} ms")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
