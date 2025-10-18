import { useSelector } from "react-redux";
import MetricCard from "../../components/MetricCard";
import TrafficGauge from "../../components/TrafficGauge";
import TrafficHistoryChart from "../../components/TrafficHistoryTable";
import WeatherTrafficCorrelation from "../../components/WeatherCorrelation";
import WeatherPanel from "../weather/WeatherPanel";

export default function TrafficDashboard() {
  const { data, history, status } = useSelector((state) => state.traffic);

  if (status === "loading" && !data)
    return <div className="text-center text-gray-500 mt-20">Loading traffic data...</div>;

  if (!data) return null;

  return (
    <main className="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-6">
        🚦 London Traffic Dashboard
      </h1>

      {/* Metrics Grid */}
      <section className="flex flex-wrap justify-center gap-2 mb-6">
        <MetricCard title="Congestion" value={data.congestion_percentage} unit="%" />
        <MetricCard title="Avg Delay" value={data.average_delay_minutes} unit="min" />
        <MetricCard title="Journey (With Traffic)" value={data.journey_time_with_traffic} unit="min" />
        <MetricCard title="Journey (No Traffic)" value={data.journey_time_without_traffic} unit="min" />
        <MetricCard title="Incidents" value={data.incidents_detected} />
        <MetricCard title="Speed" value={data.traffic_speed_kmh} unit="km/h" />
      </section>

      {/* Charts Row */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full max-w-6xl mb-10">
        <TrafficGauge congestion={data.congestion_percentage} />
        <TrafficHistoryChart data={history} />
      </section>

      {/* Weather */}
      <WeatherPanel />

      {/* Correlation Bonus */}
      <section className="w-full max-w-4xl mt-10">
        <WeatherTrafficCorrelation data={history} />
      </section>
    </main>
  );
}
