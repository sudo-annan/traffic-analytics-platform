// src/components/TrafficTrendChart.jsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { useEffect, useState } from "react";

export default function TrafficTrendChart({ data }) {
  const [animateOnce, setAnimateOnce] = useState(true);

  useEffect(() => {
    // whenever data updates, trigger animation once
    setAnimateOnce(true);

    // after animation duration, freeze animation
    const timer = setTimeout(() => setAnimateOnce(false), 2200);
    return () => clearTimeout(timer);
  }, [data]);

  return (
    <div className="bg-white p-4 rounded-xl shadow-md h-[350px]">
      <h2 className="text-sm font-semibold mb-2">Traffic Trend Over Time</h2>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(t) => new Date(t).toLocaleTimeString()}
            minTickGap={30}
          />
          <YAxis />
          <Tooltip labelFormatter={(t) => new Date(t).toLocaleString()} />

          <Line
            type="linear" // ensures all points are connected directly
            dataKey="congestion_percentage"
            stroke="#ef4444"
            strokeWidth={2.5}
            dot={{ r: 4 }}
            isAnimationActive={animateOnce}
            animationDuration={2000}
          />
          <Line
            type="linear"
            dataKey="average_delay_minutes"
            stroke="#3b82f6"
            strokeWidth={2.5}
            dot={{ r: 4 }}
            isAnimationActive={animateOnce}
            animationDuration={2000}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
