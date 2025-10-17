import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function WeatherTrafficCorrelation({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-md w-full">
      <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-3">
        Weather vs Traffic Correlation
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid />
          <XAxis dataKey="temp_c" name="Temperature (°C)" />
          <YAxis dataKey="congestion_percentage" name="Congestion (%)" />
          <Tooltip cursor={{ strokeDasharray: "3 3" }} />
          <Scatter name="Observations" data={data} fill="#22c55e" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
