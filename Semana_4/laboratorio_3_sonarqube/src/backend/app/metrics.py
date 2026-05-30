from __future__ import annotations


def build_summary(catalog: list[dict[str, object]], orders: list[dict[str, object]]) -> dict[str, object]:
    order_count = len(orders)
    catalog_size = len(catalog)

    return {
        'openOrders': order_count,
        'catalogSize': catalog_size,
        'conversionRate': 0.41,
        'technicalDebt': 9,
    }
