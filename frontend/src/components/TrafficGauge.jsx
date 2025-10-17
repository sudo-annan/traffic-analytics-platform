import React from "react";
import {
  RadialBarChart,
  RadialBar,
  ResponsiveContainer,
  PolarAngleAxis,
} from "recharts";

export default function TrafficGauge({ congestion }) {
  // Determine color dynamically
  const getGaugeColor = (value) => {
    if (value < 30) return "#4ade80"; // green
    if (value < 60) return "#facc15"; // yellow
    return "#ef4444"; // red
  };

  const color = getGaugeColor(congestion);

  // Normalize congestion to 0–100
  const data = [{ name: "Congestion", value: congestion }];

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-md w-full transition-all hover:shadow-lg hover:scale-[1.01]">
      <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-3">
        Traffic Congestion Level
      </h3>

      <div className="flex justify-center items-center">
        <ResponsiveContainer width="100%" height={250}>
          <RadialBarChart
            cx="50%"
            cy="100%"
            innerRadius="100%"
            outerRadius="140%"
            barSize={25}
            startAngle={180}
            endAngle={0}
            data={data}
          >
            <PolarAngleAxis
              type="number"
              domain={[0, 100]}
              angleAxisId={0}
              tick={false}
            />
            <RadialBar
              minAngle={15}
              background
              clockWise
              dataKey="value"
              fill={color}
              cornerRadius={10}
            />
          </RadialBarChart>
        </ResponsiveContainer>
      </div>

      <p
        className={`text-center text-2xl font-bold mt-[-50px] ${
          color === "#ef4444"
            ? "text-red-500"
            : color === "#facc15"
            ? "text-yellow-400"
            : "text-green-400"
        }`}
      >
        {congestion.toFixed(1)}%
      </p>
    </div>
  );
}
