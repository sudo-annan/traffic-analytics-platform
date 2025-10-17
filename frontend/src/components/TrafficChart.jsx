import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function TrafficChart({ data }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-md w-full mt-6">
      <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-3">Traffic Trend</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="congestion_percentage" stroke="#2563eb" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
