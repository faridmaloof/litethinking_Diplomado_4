const apiBaseUrl = (process.env.API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '');

async function profile(mode: 'cached' | 'nocache'): Promise<number[]> {
  const samples: number[] = [];
  for (let i = 0; i < 5; i += 1) {
    const started = performance.now();
    const response = await fetch(`${apiBaseUrl}/api/lab?mode=${mode}&locale=es`);
    if (!response.ok) {
      throw new Error(`TYPESCRIPT profile_cache failed for mode=${mode}`);
    }
    samples.push(performance.now() - started);
  }
  return samples;
}

function average(values: number[]): number {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

const cached = await profile('cached');
const nocache = await profile('nocache');

const cachedAvg = average(cached);
const nocacheAvg = average(nocache);

if (cachedAvg >= nocacheAvg) {
  throw new Error('TYPESCRIPT profile_cache expected cached avg lower than nocache avg');
}

console.log('TYPESCRIPT profile_cache OK');
console.log(`cached avg=${cachedAvg.toFixed(2)} ms`);
console.log(`nocache avg=${nocacheAvg.toFixed(2)} ms`);
