const apiBase = '/api';

export async function loadDashboardData() {
  const [healthResponse, summaryResponse, catalogResponse, ordersResponse] = await Promise.all([
    fetch(`${apiBase}/health`),
    fetch(`${apiBase}/summary`),
    fetch(`${apiBase}/catalog`),
    fetch(`${apiBase}/orders`),
  ]);

  if (!healthResponse.ok || !summaryResponse.ok || !catalogResponse.ok || !ordersResponse.ok) {
    throw new Error('No fue posible cargar la informacion del laboratorio');
  }

  return {
    health: await healthResponse.json(),
    summary: await summaryResponse.json(),
    catalog: await catalogResponse.json(),
    orders: await ordersResponse.json(),
  };
}

export async function submitLogin(email, password) {
  const response = await fetch(`${apiBase}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  return {
    ok: response.ok,
    payload: await response.json(),
  };
}
