import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function TrafficHistoryChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-md w-full">
      <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-3">
        Traffic Pattern Over Time
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(t) =>
              new Date(t).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
            }
          />
          <YAxis />
          <Tooltip
            labelFormatter={(t) =>
              new Date(t).toLocaleString([], { hour: "2-digit", minute: "2-digit" })
            }
          />
          <Line type="monotone" dataKey="congestion_percentage" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
