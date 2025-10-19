import { useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchDashboardData } from "../features/dashboard/dashboardThunks";
import CitySelector from "../components/CitySelector";
import MetricCards from "../components/MetricCards";
import TrafficGauge from "../components/TrafficGauge";
import TrafficTrendChart from "../components/TrafficTrendChart";
import WeatherCorrelation from "../components/WeatherCorrelation";
import TrafficHistoryTable from "../components/TrafficHistoryTable";

// Constants
const REFRESH_INTERVAL = 60; // seconds

export default function Dashboard() {
  const dispatch = useDispatch();
  const { city, loading, summary, history, lastUpdated } = useSelector((s) => s.dashboard);
  
  // Refs for cleanup
  const intervalRef = useRef(null);
  const secondsLeftRef = useRef(REFRESH_INTERVAL);
  
  // Update ref when state changes
  const secondsLeft = useSelector((s) => s.dashboard.secondsLeft || REFRESH_INTERVAL);

  // Fetch data when city changes
  useEffect(() => {
    if (city) {
      dispatch(fetchDashboardData(city));
    }
    
    // Cleanup on city change or unmount
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [city, dispatch]);

  // Auto-refresh logic
  useEffect(() => {
    if (!city || loading) {
      // Clear interval when no city selected or during loading
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    // Reset countdown when data is freshly loaded
    secondsLeftRef.current = REFRESH_INTERVAL;

    // Set up auto-refresh interval
    intervalRef.current = setInterval(() => {
      secondsLeftRef.current -= 1;

      if (secondsLeftRef.current <= 0) {
        // Time to refresh
        dispatch(fetchDashboardData(city));
        secondsLeftRef.current = REFRESH_INTERVAL;
      }
      
      // Force re-render to update displayed countdown
      // This would require storing secondsLeft in Redux or using state
      // For now, we'll use a simple approach with state
    }, 1000);

    // Cleanup interval on unmount or dependency change
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [city, loading, dispatch, lastUpdated]); // Add lastUpdated to reset on new data

  // Format last updated time
  const formatLastUpdated = () => {
    if (!lastUpdated) return "Never";
    return new Date(lastUpdated).toLocaleTimeString();
  };

  // Calculate seconds left for display (simplified approach)
  const displaySecondsLeft = () => {
    if (!city || loading) return REFRESH_INTERVAL;
    return secondsLeftRef.current;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 🟦 Top Bar */}
      <div className="flex justify-between items-center bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-6 py-3 shadow-md">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold">
            {city ? `${city.name} Traffic Dashboard` : "Traffic Dashboard"}
          </h1>
          {lastUpdated && (
            <span className="text-sm text-blue-100">
              Last updated: {formatLastUpdated()}
            </span>
          )}
        </div>
        
        <div className="flex items-center gap-4">
          {city && !loading && (
            <div className="flex items-center gap-2">
              <p className="text-sm font-medium">
                Auto-refresh in:{" "}
                <span className="font-semibold bg-blue-500 px-2 py-1 rounded">
                  {displaySecondsLeft()}s
                </span>
              </p>
            </div>
          )}
          
          {loading && (
            <div className="flex items-center gap-2">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
              <span className="text-sm">Updating data...</span>
            </div>
          )}
          
          <CitySelector />
        </div>
      </div>

      {/* 🧠 Main Content */}
      <div className="p-6 space-y-6">
        {city ? (
          <>
            <MetricCards summary={summary} />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <TrafficGauge value={summary?.congestion_percentage ?? 0} />
              <TrafficTrendChart data={history} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <WeatherCorrelation data={history} />
              <TrafficHistoryTable data={history} />
            </div>
          </>
        ) : (
          // Empty state when no city selected
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">
              Please select a city to view traffic data
            </div>
          </div>
        )}
      </div>

      {/* 🔄 Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-white bg-opacity-70 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg flex items-center gap-3">
            <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-600 border-t-transparent"></div>
            <div className="text-lg font-semibold text-gray-700">
              Fetching latest traffic & weather data...
            </div>
          </div>
        </div>
      )}
    </div>
  );
}