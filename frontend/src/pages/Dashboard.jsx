import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchDashboardData } from "../features/dashboard/dashboardThunks";
import CitySelector from "../components/CitySelector";
import MetricCards from "../components/MetricCards";
import TrafficGauge from "../components/TrafficGauge";
import TrafficTrendChart from "../components/TrafficTrendChart";
import WeatherCorrelation from "../components/WeatherCorrelation";
import TrafficHistoryTable from "../components/TrafficHistoryTable";

export default function Dashboard() {
  const dispatch = useDispatch();
  const { city, loading, summary, history } = useSelector((s) => s.dashboard);
  const [secondsLeft, setSecondsLeft] = useState(60);
  const [activeInterval, setActiveInterval] = useState(null);

  // Fetch on city change
  useEffect(() => {
    if (city) dispatch(fetchDashboardData(city));
  }, [city, dispatch]);

  // Countdown & refresh after load finishes
  useEffect(() => {
    if (!city) return;

    // stop countdown during loading
    if (loading) {
      if (activeInterval) clearInterval(activeInterval);
      return;
    }

    // reset counter and start countdown only after load finished
    setSecondsLeft(60);
    const tick = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          dispatch(fetchDashboardData(city));
          return 60;
        }
        return prev - 1;
      });
    }, 1000);

    setActiveInterval(tick);
    return () => clearInterval(tick);
  }, [city, loading, dispatch]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 🟦 Top Bar */}
      <div className="flex justify-between items-center bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-6 py-3 shadow-md">
        <h1 className="text-2xl font-bold">
          {city ? `${city.name} Traffic Dashboard` : "Traffic Dashboard"}
        </h1>
        <div className="flex items-center gap-4">
          {!loading && city && (
            <p className="text-sm font-medium">
              Data auto-updates in:{" "}
              <span className="font-semibold">{secondsLeft}s</span>
            </p>
          )}
          <CitySelector />
        </div>
      </div>

      {/* 🧠 Main Content */}
      <div className="p-6 space-y-6">
        <MetricCards summary={summary} />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <TrafficGauge value={summary?.congestion_percentage ?? 0} />
          <TrafficTrendChart data={history} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <WeatherCorrelation data={history} />
          <TrafficHistoryTable data={history} />
        </div>
      </div>

      {/* 🔄 Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-white bg-opacity-70 flex justify-center items-center z-50">
          <div className="text-lg font-semibold text-gray-700">
            Fetching new traffic & weather data...
          </div>
        </div>
      )}
    </div>
  );
}
