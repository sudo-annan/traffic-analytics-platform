import { useDispatch, useSelector } from "react-redux";
import { setCity } from "../features/dashboard/dashboardSlice";
import { CITIES } from "../config/cities";

export default function CitySelector() {
  const dispatch = useDispatch();
  const selectedCity = useSelector((state) => state.dashboard.city);

  const handleChange = (e) => {
    const selected = CITIES.find((c) => c.name === e.target.value);
    if (selected) {
      dispatch(setCity(selected));
    }
  };

  return (
    <select
      value={selectedCity?.name || ""}
      onChange={handleChange}
      className="px-3 py-2 rounded-md border border-gray-300 text-gray-800 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="" disabled>
        Select City
      </option>
      {CITIES.map((c) => (
        <option key={c.name} value={c.name}>
          {c.name}
        </option>
      ))}
    </select>
  );
}