export default function TrafficHistoryTable({ data }) {
  return (
    <div className="bg-white p-4 rounded-2xl shadow-md overflow-y-auto">
      <h3 className="text-lg font-semibold mb-3">Traffic History</h3>
      <table className="w-full text-sm text-left">
        <thead>
          <tr className="border-b text-gray-600">
            <th className="py-2">Timestamp</th>
            <th>Congestion (%)</th>
            <th>Avg Delay (min)</th>
          </tr>
        </thead>
        <tbody>
          {data?.slice(-10).map((row, i) => (
            <tr key={i} className="border-b last:border-none">
              <td className="py-1">{new Date(row.timestamp).toLocaleString()}</td>
              <td>{row.congestion_percentage.toFixed(1)}</td>
              <td>{row.average_delay_minutes.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
