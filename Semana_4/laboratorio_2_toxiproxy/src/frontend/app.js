const apiBase = '/api';

const summaryGrid = document.getElementById('summary-grid');
const catalogGrid = document.getElementById('catalog-grid');
const ordersTable = document.getElementById('orders-table');
const healthPill = document.getElementById('health-pill');
const loginForm = document.getElementById('login-form');
const loginResult = document.getElementById('login-result');

const money = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

function renderSummary(summary, health) {
  summaryGrid.innerHTML = [
    ['Pedidos abiertos', summary.openOrders],
    ['Catalogo', summary.catalogSize],
    ['Presupuesto de latencia', `${summary.latencyBudgetMs} ms`],
    ['Señales de resiliencia', summary.resilienceSignals],
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

function renderCatalog(products) {
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

function renderOrders(orders) {
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

async function loadDashboard() {
  const [healthResponse, summaryResponse, catalogResponse, ordersResponse] = await Promise.all([
    fetch(`${apiBase}/health`),
    fetch(`${apiBase}/summary`),
    fetch(`${apiBase}/catalog`),
    fetch(`${apiBase}/orders`),
  ]);

  if (!healthResponse.ok || !summaryResponse.ok || !catalogResponse.ok || !ordersResponse.ok) {
    throw new Error('No fue posible cargar la informacion del laboratorio');
  }

  const health = await healthResponse.json();
  const summary = await summaryResponse.json();
  const catalog = await catalogResponse.json();
  const orders = await ordersResponse.json();

  renderSummary(summary, health);
  renderCatalog(catalog.products);
  renderOrders(orders.orders);
}

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);

  loginResult.textContent = 'Validando credenciales de prueba...';

  const response = await fetch(`${apiBase}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: formData.get('email'),
      password: formData.get('password'),
    }),
  });

  const payload = await response.json();

  if (!response.ok) {
    loginResult.textContent = `Error: ${payload.detail || 'Login rechazado'}`;
    return;
  }

  loginResult.textContent = JSON.stringify(payload, null, 2);
});

loadDashboard().catch((error) => {
  healthPill.textContent = 'Sin conexion';
  loginResult.textContent = error.message;
});
