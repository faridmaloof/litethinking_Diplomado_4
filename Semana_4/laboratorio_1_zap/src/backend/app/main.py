from __future__ import annotations

from datetime import datetime, timezone
from secrets import token_urlsafe

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .catalog import ACCOUNTS, CATALOG, ORDERS

app = FastAPI(title='Semana 4 - Laboratorio 1', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get('/api/health')
def health() -> dict[str, object]:
    return {
        'status': 'UP',
        'lab': 'lab-1-zap',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'components': ['frontend', 'backend'],
    }


@app.get('/api/catalog')
def catalog() -> dict[str, object]:
    return {
        'store': 'Academia Store',
        'featuredCampaign': 'DevSecOps Starter Pack',
        'products': CATALOG,
    }


@app.get('/api/orders')
def orders() -> dict[str, object]:
    return {
        'currency': 'USD',
        'orders': ORDERS,
        'activeCheckouts': 3,
    }


@app.post('/api/login')
def login(payload: LoginRequest) -> dict[str, object]:
    account = ACCOUNTS.get(payload.email.lower())
    if account is None or account['password'] != payload.password:
        raise HTTPException(status_code=401, detail='Credenciales no validas')

    return {
        'sessionId': token_urlsafe(16),
        'user': {
            'email': payload.email.lower(),
            'displayName': account['displayName'],
            'role': account['role'],
        },
    }


@app.get('/api/summary')
def summary() -> dict[str, object]:
    return {
        'openOrders': len(ORDERS),
        'catalogSize': len(CATALOG),
        'conversionRate': 0.37,
        'securityWarnings': 4,
    }
