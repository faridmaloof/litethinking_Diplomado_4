from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone
from typing import Literal

from .config import AppConfig

AppMode = Literal['cached', 'nocache']
Locale = Literal['es', 'de']


class LabService:
    # Servicio de dominio: concentra reglas del laboratorio
    # (cache, payload de performance, accesibilidad y SEO).
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._cache: dict[tuple[AppMode, Locale], dict[str, object]] = {}

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat(timespec='seconds')

    def _copy_for_locale(self, locale: Locale) -> dict[str, str]:
        if locale == 'de':
            return {
                'headline': 'Leistungspruefung mit Cache und ohne Cache',
                'subheadline': 'Das Labor zeigt, wie sich TTFB, p95 und Durchsatz aendern.',
                'intro': 'Die Demo fuehrt echtes Verhalten fuer Performance, Accessibility und SEO zusammen.',
                'label': 'Sehr lange Lokalisierungszeichenkette fuer Layout-Tests',
            }

        return {
            'headline': 'Laboratorio de rendimiento con cache y sin cache',
            'subheadline': 'La demo expone TTFB, p95 y throughput para que el taller sea medible.',
            'intro': 'La experiencia une performance, accesibilidad y SEO en una sola pantalla.',
            'label': 'Cadena de localizacion larga para probar el diseno',
        }

    def _seo_payload(self, mode: AppMode, locale: Locale) -> dict[str, object]:
        locale_copy = self._copy_for_locale(locale)
        title = 'PulseLab QA Studio | Rendimiento, accesibilidad y SEO'
        description = (
            'Laboratorio en React, Vite y FastAPI para probar cache, sin cache, accesibilidad y SEO con '
            'validaciones reales.'
        )

        return {
            'title': title,
            'description': description,
            'canonical': f'{self._config.app_origin}/?mode={mode}&locale={locale}',
            'robots': 'index,follow',
            'keywords': ['performance', 'accessibility', 'seo', 'cache', 'fastapi', 'vite', 'react'],
            'jsonLd': {
                '@context': 'https://schema.org',
                '@type': 'LearningResource',
                'name': title,
                'description': description,
                'learningResourceType': 'QA laboratory',
                'inLanguage': locale,
                'isAccessibleForFree': True,
                'keywords': ', '.join(['performance', 'accessibility', 'seo', 'cache']),
                'alternateName': locale_copy['headline'],
            },
        }

    def _accessibility_payload(self) -> dict[str, object]:
        return {
            'landmarks': ['skip link', 'header', 'nav', 'main', 'section', 'form', 'footer'],
            'signals': [
                'labels explicitas en todos los controles',
                'botones reales para la navegacion con teclado',
                'aria-live para estado de carga y respuesta',
                'jerarquia de titulos coherente',
                'contraste alto y enfoque visible',
            ],
            'testing': [
                'Tab para recorrer todos los controles',
                'Lectura de encabezados por lector de pantalla',
                'Validacion de texto alterno y etiquetas',
            ],
        }

    def _performance_payload(self, mode: AppMode, server_delay_ms: int) -> dict[str, object]:
        if mode == 'cached':
            return {
                'cacheHit': True,
                'serverDelayMs': server_delay_ms,
                'ttfbMs': 52,
                'p95Ms': 118,
                'throughputRps': 235,
                'note': 'Cache activa: respuesta rapida para medir la mejor ruta.',
            }

        return {
            'cacheHit': False,
            'serverDelayMs': server_delay_ms,
            'ttfbMs': 448,
            'p95Ms': 980,
            'throughputRps': 58,
            'note': 'Sin cache: respuesta deliberadamente mas lenta para el taller.',
        }

    def _content_payload(self, mode: AppMode, locale: Locale) -> dict[str, object]:
        copy = self._copy_for_locale(locale)
        return {
            'headline': copy['headline'],
            'subheadline': copy['subheadline'],
            'intro': copy['intro'],
            'localeLabel': copy['label'],
            'cacheModeLabel': 'Modo cache' if mode == 'cached' else 'Modo sin cache',
        }

    async def build_lab_payload(self, mode: AppMode, locale: Locale) -> dict[str, object]:
        # Estrategia cache-first para mode=cached.
        # Si existe un valor vigente, se retorna sin simular latencia.
        cache_key = (mode, locale)
        now = time.monotonic()
        cached_entry = self._cache.get(cache_key)

        if mode == 'cached' and cached_entry:
            age_seconds = round(now - float(cached_entry['createdAt']), 2)
            if age_seconds <= self._config.cache_ttl_seconds:
                payload = dict(cached_entry['payload'])
                payload['cache'] = {
                    'hit': True,
                    'ttlSeconds': self._config.cache_ttl_seconds,
                    'ageSeconds': age_seconds,
                }
                return payload

        server_delay_ms = 90 if mode == 'cached' else 720
        # Latencia artificial controlada para que QA pueda
        # comparar claramente cached vs nocache.
        await asyncio.sleep(server_delay_ms / 1000)

        payload = {
            'mode': mode,
            'locale': locale,
            'generatedAt': self._now_iso(),
            'cache': {
                'hit': False,
                'ttlSeconds': self._config.cache_ttl_seconds,
                'ageSeconds': 0,
            },
            'performance': self._performance_payload(mode, server_delay_ms),
            'accessibility': self._accessibility_payload(),
            'seo': self._seo_payload(mode, locale),
            'content': self._content_payload(mode, locale),
        }

        if mode == 'cached':
            self._cache[cache_key] = {
                'createdAt': now,
                'payload': payload,
            }

        return payload

    def health_payload(self) -> dict[str, object]:
        return {
            'status': 'UP',
            'service': 'pulselab-api',
            'timestamp': self._now_iso(),
        }
