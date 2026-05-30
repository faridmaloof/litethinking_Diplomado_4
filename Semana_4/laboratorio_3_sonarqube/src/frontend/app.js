import { loadDashboardData, submitLogin } from './api.js';
import { renderCatalog, renderOrders, renderSummary } from './renderers.js';

const summaryGrid = document.getElementById('summary-grid');
const catalogGrid = document.getElementById('catalog-grid');
const ordersTable = document.getElementById('orders-table');
const healthPill = document.getElementById('health-pill');
const loginForm = document.getElementById('login-form');
const loginResult = document.getElementById('login-result');

async function loadPage() {
  const { health, summary, catalog, orders } = await loadDashboardData();
  renderSummary(summaryGrid, healthPill, summary, health);
  renderCatalog(catalogGrid, catalog.products);
  renderOrders(ordersTable, orders.orders);
}

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);

  loginResult.textContent = 'Validando credenciales de prueba...';

  const { ok, payload } = await submitLogin(formData.get('email'), formData.get('password'));

  if (!ok) {
    loginResult.textContent = `Error: ${payload.detail || 'Login rechazado'}`;
    return;
  }

  loginResult.textContent = JSON.stringify(payload, null, 2);
});

try {
  await loadPage()
} catch (error) {
  healthPill.textContent = 'Sin conexion';
  loginResult.textContent = error.message;
}
