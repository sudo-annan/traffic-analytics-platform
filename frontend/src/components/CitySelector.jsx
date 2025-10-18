// src/components/CitySelector.jsx
import { useDispatch, useSelector } from "react-redux";
import { setCity } from "../features/dashboard/dashboardSlice";

const cities = [
  { name: "London", lat: 51.5074, lon: -0.1278 },
  { name: "Birmingham", lat: 52.4862, lon: -1.8904 },
  { name: "Manchester", lat: 53.4808, lon: -2.2426 },
  { name: "Liverpool", lat: 53.4084, lon: -2.9916 },
  { name: "Leeds", lat: 53.8008, lon: -1.5491 },
  { name: "Sheffield", lat: 53.3811, lon: -1.4701 },
  { name: "Newcastle upon Tyne", lat: 54.9784, lon: -1.6174 },
  { name: "Nottingham", lat: 52.9548, lon: -1.1581 },
  { name: "Bristol", lat: 51.4545, lon: -2.5879 },
  { name: "Cardiff", lat: 51.4816, lon: -3.1791 },
  { name: "Edinburgh", lat: 55.9533, lon: -3.1883 },
  { name: "Glasgow", lat: 55.8642, lon: -4.2518 },
  { name: "Belfast", lat: 54.5973, lon: -5.9301 },
  { name: "Cambridge", lat: 52.2053, lon: 0.1218 },
  { name: "Oxford", lat: 51.752, lon: -1.2577 },
  { name: "Brighton", lat: 50.8225, lon: -0.1372 },
  { name: "Southampton", lat: 50.9097, lon: -1.4044 },
  { name: "Leicester", lat: 52.6369, lon: -1.1398 },
  { name: "Reading", lat: 51.4543, lon: -0.9781 },
  { name: "Plymouth", lat: 50.3755, lon: -4.1427 },
];

export default function CitySelector() {
  const dispatch = useDispatch();
  const selectedCity = useSelector((state) => state.dashboard.city);

  const handleChange = (e) => {
    const selected = cities.find((c) => c.name === e.target.value);
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
      {cities.map((c) => (
        <option key={c.name} value={c.name}>
          {c.name}
        </option>
      ))}
    </select>
  );
}
