import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Global metrics
export let errorRate = new Rate('errors');

// Test configuration
export let options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp-up to 50 users
    { duration: '1m', target: 100 },  // Steady state at 100 users
    { duration: '30s', target: 500 }, // Peak burst to 500 users
    { duration: '30s', target: 0 },   // Ramp-down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be < 500ms
    errors: ['rate<0.01'],            // Error rate must be less than 1%
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api/v1';

export default function () {
  const token = __ENV.API_TOKEN || 'test-token';
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  };

  // Simulate a typical user workflow
  // 1. Get Dashboard
  let res = http.get(`${BASE_URL}/dashboards/me`, params);
  check(res, { 'status is 200': (r) => r.status === 200 }) || errorRate.add(1);
  sleep(1);

  // 2. Fetch attendance
  res = http.get(`${BASE_URL}/attendance`, params);
  check(res, { 'status is 200': (r) => r.status === 200 }) || errorRate.add(1);
  sleep(2);
}
