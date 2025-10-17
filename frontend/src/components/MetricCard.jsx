export default function MetricCard({ title, value, unit }) {
  return (
    <div className="bg-white dark:bg-gray-800 shadow-md rounded-2xl p-4 flex flex-col items-center justify-center w-full sm:w-1/3 md:w-1/4 lg:w-1/6 m-2">
      <h3 className="text-gray-600 dark:text-gray-300 text-sm font-medium mb-1">{title}</h3>
      <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
        {value}
        {unit && <span className="text-sm font-normal ml-1">{unit}</span>}
      </p>
    </div>
  );
}
