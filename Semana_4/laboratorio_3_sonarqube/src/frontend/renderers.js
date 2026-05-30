const money = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

export function renderSummary(summaryGrid, healthPill, summary, health) {
  summaryGrid.innerHTML = [
    ['Pedidos abiertos', summary.openOrders],
    ['Catalogo', summary.catalogSize],
    ['Conversion', `${Math.round(summary.conversionRate * 100)}%`],
    ['Deuda tecnica', summary.technicalDebt],
  ]
    .map(
      ([label, value]) => `
        <article class="stat-card">
          <span>${label}</span>
          <strong>${value}</strong>
        </article>
      `,
    )
    .join('');

  healthPill.textContent = `${health.status} · ${health.lab}`;
}

export function renderCatalog(catalogGrid, products) {
  catalogGrid.innerHTML = products
    .map(
      (product) => `
        <article class="product-card">
          <span class="tag">${product.tag}</span>
          <strong>${product.name}</strong>
          <p>SKU ${product.id}</p>
          <p>Inventario: ${product.stock} unidades</p>
          <p>Precio: ${money.format(product.priceUsd)}</p>
        </article>
      `,
    )
    .join('');
}

export function renderOrders(ordersTable, orders) {
  ordersTable.innerHTML = orders
    .map(
      (order) => `
        <article class="order-row">
          <span class="tag">${order.status}</span>
          <strong>${order.customer}</strong>
          <p>Pedido ${order.id}</p>
          <p>${order.items} item(s)</p>
          <p>Total ${money.format(order.totalUsd)}</p>
        </article>
      `,
    )
    .join('');
}
