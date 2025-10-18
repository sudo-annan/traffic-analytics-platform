const BASE_URL = "http://localhost:8000/api";

const CITY_COORDS = {
  London: { lat: 51.5074, lon: -0.1278 },
  Birmingham: { lat: 52.485, lon: -1.862 },
  Manchester: { lat: 53.4808, lon: -2.2426 },
  Leeds: { lat: 53.8008, lon: -1.5491 },
  Liverpool: { lat: 53.4084, lon: -2.9916 },
};

export async function refreshData(city) {
  const { lat, lon } = CITY_COORDS[city];
  const url = `${BASE_URL}/data/refresh?city=${city}&lat=${lat}&lon=${lon}`;
  const res = await fetch(url, { method: "POST" });
  if (!res.ok) throw new Error("Failed to refresh data");
}

export async function fetchSummary(city) {
  const res = await fetch(`${BASE_URL}/traffic/summary?city=${city}`);
  if (!res.ok) throw new Error("Failed to fetch summary");
  return res.json();
}

export async function fetchHistory(city) {
  const res = await fetch(`${BASE_URL}/traffic/history?city=${city}`);
  if (!res.ok) throw new Error("Failed to fetch history");
  return res.json();
}
