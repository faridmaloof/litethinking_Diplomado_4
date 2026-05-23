const frontendBaseUrl = (process.env.FRONTEND_BASE_URL || 'http://localhost:4173').replace(/\/$/, '');

const indexResponse = await fetch(`${frontendBaseUrl}/`);
const robotsResponse = await fetch(`${frontendBaseUrl}/robots.txt`);
const sitemapResponse = await fetch(`${frontendBaseUrl}/sitemap.xml`);

if (!indexResponse.ok || !robotsResponse.ok || !sitemapResponse.ok) {
  throw new Error('JAVASCRIPT audit_frontend failed on HTTP status');
}

const indexHtml = await indexResponse.text();
const robotsTxt = await robotsResponse.text();
const sitemapXml = await sitemapResponse.text();

const requiredInHtml = [
  '<meta name="description"',
  '<link rel="canonical"',
  'application/ld+json'
];

for (const marker of requiredInHtml) {
  if (!indexHtml.includes(marker)) {
    throw new Error(`JAVASCRIPT audit_frontend missing marker: ${marker}`);
  }
}

if (!robotsTxt.includes('Sitemap:')) {
  throw new Error('JAVASCRIPT audit_frontend robots missing sitemap');
}

if (!sitemapXml.includes('<loc>http://localhost:4173/</loc>')) {
  throw new Error('JAVASCRIPT audit_frontend sitemap root URL missing');
}

console.log('JAVASCRIPT audit_frontend OK');
