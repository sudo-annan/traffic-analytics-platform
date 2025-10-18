// src/components/WeatherCorrelation.jsx
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";
import { useEffect, useState } from "react";

export default function WeatherCorrelation({ data }) {
  const [animateOnce, setAnimateOnce] = useState(true);

  useEffect(() => {
    setAnimateOnce(true);
    const timer = setTimeout(() => setAnimateOnce(false), 2200);
    return () => clearTimeout(timer);
  }, [data]);

  return (
    <div className="bg-white p-4 rounded-xl shadow-md h-[350px]">
      <h2 className="text-sm font-semibold mb-2">Weather vs Congestion</h2>
      <ResponsiveContainer width="100%" height="90%">
        <ComposedChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(t) => new Date(t).toLocaleTimeString()}
            minTickGap={30}
          />
          <YAxis yAxisId="left" orientation="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip labelFormatter={(t) => new Date(t).toLocaleString()} />
          <Legend />
          <Bar
            yAxisId="left"
            dataKey="congestion_percentage"
            fill="#ef4444"
            isAnimationActive={animateOnce}
            animationDuration={2000}
          />
          <Line
            yAxisId="right"
            type="linear"
            dataKey="average_delay_minutes"
            stroke="#3b82f6"
            strokeWidth={2.5}
            dot={{ r: 4 }}
            isAnimationActive={animateOnce}
            animationDuration={2000}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
