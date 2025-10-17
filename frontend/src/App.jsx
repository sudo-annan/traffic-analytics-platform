import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import {
  fetchTrafficSummary,
  fetchTrafficHistory,
} from "./features/traffic/trafficSlice";
import { fetchWeather } from "./features/weather/weatherSlice";
import TrafficDashboard from "./features/traffic/TrafficDashboard";

export default function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    // Initial load
    dispatch(fetchTrafficSummary());
    dispatch(fetchTrafficHistory());
    dispatch(fetchWeather());

    // Auto refresh every 60 seconds
    const interval = setInterval(() => {
      dispatch(fetchTrafficSummary());
      dispatch(fetchTrafficHistory());
      dispatch(fetchWeather());
    }, 60000);

    return () => clearInterval(interval);
  }, [dispatch]);

  return (
    <div
      className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100"
      role="main"
      aria-label="Traffic and weather analytics dashboard"
    >
      <TrafficDashboard />
    </div>
  );
}
