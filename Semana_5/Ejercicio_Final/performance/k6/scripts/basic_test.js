import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },    // Ramp-up to 20 VUs
    { duration: '1m', target: 20 },     // Stay at 20 VUs
    { duration: '30s', target: 0 },     // Ramp-down to 0 VUs
  ],
};

export default function () {
  // Test against httpbin.org through the proxy
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // Basic GET request
  const response = http.get('http://httpbin.org/get', params);
  
  // Check that response is successful
  check(response, {
    'status is 200': (r) => r.status === 200,
    'has headers': (r) => r.json().headers !== undefined,
  });

  // POST request with data
  const postData = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      test: 'data',
      timestamp: Date.now(),
    }),
  };
  
  const postResponse = http.post('http://httpbin.org/post', postData.body, {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(postResponse, {
    'post status is 200': (r) => r.status === 200,
  });

  sleep(1);
}