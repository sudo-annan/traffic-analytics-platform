// src/components/TrafficGauge.jsx
import { Gauge, gaugeClasses } from "@mui/x-charts";

export default function TrafficGauge({ value }) {
  // Choose color based on congestion %
  let color = "#22c55e"; // green
  if (value > 66.66) color = "#ef4444"; // red
  else if (value > 33.33) color = "#facc15"; // yellow

  return (
    <div className="bg-white p-4 rounded-xl shadow-md flex flex-col items-center justify-center h-[350px]">
      <h2 className="text-sm font-semibold mb-2 self-start">Traffic Congestion Level</h2>
      <div className="flex-1 flex justify-center items-center w-full">
        <Gauge
          width={250}
          height={160}
          startAngle={-110}
          endAngle={110}
          value={value}
          valueMin={0}
          valueMax={100}
          cornerRadius={20}
          sx={{
            [`& .${gaugeClasses.valueText}`]: {
              fontSize: 20,
              fontWeight: "bold",
              fill: "#dc2626",
            },
            [`& .${gaugeClasses.valueArc}`]: {
              fill: color,
            },
            [`& .${gaugeClasses.track}`]: {
              fill: "#e5e7eb",
            },
          }}
        />
      </div>
      <p className="mt-2 text-lg font-semibold text-gray-700">{value.toFixed(1)}%</p>

      {/* Legend */}
      <div className="flex justify-center gap-4 text-sm mt-3">
        <div className="flex items-center gap-1">
          <span className="w-3 h-3 bg-green-500 rounded-full"></span> <span>Low (0–33%)</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="w-3 h-3 bg-yellow-400 rounded-full"></span> <span>Moderate (33–66%)</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="w-3 h-3 bg-red-500 rounded-full"></span> <span>Severe (g.t 66%)</span>
        </div>
      </div>
    </div>
  );
}
