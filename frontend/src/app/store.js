import { configureStore } from "@reduxjs/toolkit";
import trafficReducer from "../features/traffic/trafficSlice";
import weatherReducer from "../features/weather/weatherSlice";

export const store = configureStore({
  reducer: {
    traffic: trafficReducer,
    weather: weatherReducer,
  },
});

export default store;
