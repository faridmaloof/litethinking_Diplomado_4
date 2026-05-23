const apiBaseUrl = (process.env.API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

const health = await fetch(`${apiBaseUrl}/api/health`);
const cached = await fetch(`${apiBaseUrl}/api/lab?mode=cached&locale=es`);
const nocache = await fetch(`${apiBaseUrl}/api/lab?mode=nocache&locale=es`);

if (!health.ok || !cached.ok || !nocache.ok) {
  throw new Error('JAVASCRIPT validate_api failed on HTTP status');
}

const healthPayload = await health.json();
const cachedPayload = await cached.json();
const nocachePayload = await nocache.json();

if (healthPayload.status !== 'UP') {
  throw new Error('JAVASCRIPT validate_api health check failed');
}

if (cachedPayload.performance.ttfbMs >= nocachePayload.performance.ttfbMs) {
  throw new Error('JAVASCRIPT validate_api expected cached ttfb lower than nocache');
}

console.log('JAVASCRIPT validate_api OK');
console.log(`cached ttfb=${cachedPayload.performance.ttfbMs} ms`);
console.log(`nocache ttfb=${nocachePayload.performance.ttfbMs} ms`);
