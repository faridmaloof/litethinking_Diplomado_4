from __future__ import annotations

CATALOG = [
    {
        'id': 'sku-101',
        'name': 'Pipeline Secure Hoodie',
        'priceUsd': 42,
        'stock': 18,
        'tag': 'DevSecOps',
    },
    {
        'id': 'sku-202',
        'name': 'Chaos Monkey Notebook',
        'priceUsd': 18,
        'stock': 44,
        'tag': 'Chaos Engineering',
    },
    {
        'id': 'sku-303',
        'name': 'Shift Left Mug',
        'priceUsd': 14,
        'stock': 61,
        'tag': 'Quality Gate',
    },
]

ORDERS = [
    {
        'id': 'ord-9201',
        'customer': 'Ana Torres',
        'status': 'Aprobado',
        'items': 2,
        'totalUsd': 66,
    },
    {
        'id': 'ord-9202',
        'customer': 'Luis Rivera',
        'status': 'En validacion',
        'items': 1,
        'totalUsd': 18,
    },
    {
        'id': 'ord-9203',
        'customer': 'Maria Gomez',
        'status': 'Enviado',
        'items': 3,
        'totalUsd': 74,
    },
]

ACCOUNTS = {
    'student@demo.local': {
        'loginCode': 'DevSecOps123',
        'role': 'student',
        'displayName': 'Student Demo',
    },
    'mentor@demo.local': {
        'loginCode': 'Mentor123!',
        'role': 'instructor',
        'displayName': 'Mentor Demo',
    },
}
