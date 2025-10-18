export default function MetricCards({ summary }) {
  if (!summary) return <div>No data available yet.</div>;

  const metrics = [
    { label: "Congestion (%)", value: summary.congestion_percentage },
    { label: "Avg Delay (min)", value: summary.average_delay_minutes },
    { label: "Temperature (°C)", value: summary.weather?.temp_c },
    { label: "Humidity (%)", value: summary.weather?.humidity },
    { label: "Condition", value: summary.weather?.condition },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
      {metrics.map((m, i) => (
        <div
          key={i}
          className="bg-white p-4 rounded-2xl shadow text-center border border-gray-100"
        >
          <h3 className="text-gray-500 text-sm">{m.label}</h3>
          <p className="text-xl font-semibold text-rose-600 mt-1">
            {m.value ?? "--"}
          </p>
        </div>
      ))}
    </div>
  );
}
