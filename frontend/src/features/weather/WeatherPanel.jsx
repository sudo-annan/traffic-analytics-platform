import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchWeather } from "./weatherSlice";

export default function WeatherPanel() {
  const dispatch = useDispatch();
  const { data, status } = useSelector((state) => state.weather);

//   useEffect(() => {
//     dispatch(fetchWeather());
//     const interval = setInterval(() => dispatch(fetchWeather()), 60000); // 60s interval
//     return () => clearInterval(interval);
//   }, [dispatch]);

  if (status === "loading" && !data)
    return <div className="text-gray-500 mt-4">Loading weather...</div>;
  if (status === "failed")
    return <div className="text-red-500 mt-4">Failed to load weather data.</div>;
  if (!data) return null;

  return (
    <div className="bg-white dark:bg-gray-800 shadow-lg rounded-2xl p-6 mt-10 w-full max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-100">
            🌤 London Weather
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            {new Date(data.timestamp).toLocaleString()}
          </p>
        </div>
        <div className="text-right">
          <h3 className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {data.temp_c}°C
          </h3>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            Feels like {data.feelslike_c}°C
          </p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-4 text-gray-700 dark:text-gray-300">
        <div>🌫 Condition: <strong>{data.condition}</strong></div>
        <div>💨 Wind: <strong>{data.wind_kph} km/h</strong></div>
        <div>💧 Humidity: <strong>{data.humidity}%</strong></div>
        <div>☁️ Cloud: <strong>{data.cloud}%</strong></div>
        <div>🌡 Pressure: <strong>{data.pressure_mb} mb</strong></div>
        <div>🌞 UV Index: <strong>{data.uv}</strong></div>
      </div>
    </div>
  );
}
