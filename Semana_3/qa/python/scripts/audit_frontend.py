from __future__ import annotations

import os

import httpx
from bs4 import BeautifulSoup


def main() -> int:
    frontend_base_url = os.getenv('FRONTEND_BASE_URL', 'http://localhost:4173').rstrip('/')

    with httpx.Client(timeout=10.0) as client:
        index_html = client.get(f'{frontend_base_url}/')
        index_html.raise_for_status()

        robots_txt = client.get(f'{frontend_base_url}/robots.txt')
        robots_txt.raise_for_status()

        sitemap_xml = client.get(f'{frontend_base_url}/sitemap.xml')
        sitemap_xml.raise_for_status()

    soup = BeautifulSoup(index_html.text, 'html.parser')

    assert soup.find('meta', attrs={'name': 'description'}) is not None
    assert soup.find('link', attrs={'rel': 'canonical'}) is not None
    assert 'Sitemap:' in robots_txt.text
    assert '<loc>http://localhost:4173/</loc>' in sitemap_xml.text

    print('PYTHON audit_frontend OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
