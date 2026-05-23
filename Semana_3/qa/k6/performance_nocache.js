import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '20s', target: 10 },
    { duration: '30s', target: 25 },
    { duration: '20s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1200'],
  },
}

const baseUrl = __ENV.BASE_URL || 'http://localhost:8000'

export default function () {
  const mode = 'cached'
  const response = http.get(`${baseUrl}/api/lab?mode=${mode}&locale=es`)

  check(response, {
    'status is 200': (res) => res.status === 200,
    'contains performance payload': (res) => res.json('performance.ttfbMs') !== undefined,
  })

  sleep(1)
}