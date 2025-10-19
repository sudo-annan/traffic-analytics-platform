import { CITY_COORDS } from '../config/cities';

const BASE_URL = "http://localhost:8000/api/v1";

// Generic API request helper
async function apiRequest(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}

// Specific API functions
export const trafficApi = {
  async refreshData(city) {
    const { lat, lon } = CITY_COORDS[city];
    return apiRequest(`/data/refresh?city=${encodeURIComponent(city)}&lat=${lat}&lon=${lon}`, {
      method: "POST",
    });
  },

  async fetchSummary(city) {
    return apiRequest(`/traffic/summary?city=${encodeURIComponent(city)}`);
  },

  async fetchHistory(city) {
    return apiRequest(`/traffic/history?city=${encodeURIComponent(city)}`);
  },

  // Combined request for better performance
  async fetchDashboardData(city) {
    const [summary, history] = await Promise.all([
      this.fetchSummary(city),
      this.fetchHistory(city)
    ]);
    return { summary, history };
  },
};

// Legacy functions for backward compatibility
export async function refreshData(city) {
  return trafficApi.refreshData(city);
}

export async function fetchSummary(city) {
  return trafficApi.fetchSummary(city);
}

export async function fetchHistory(city) {
  return trafficApi.fetchHistory(city);
}