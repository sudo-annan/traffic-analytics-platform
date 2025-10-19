import { createAsyncThunk } from "@reduxjs/toolkit";
import { trafficApi } from "../../api/trafficApi";

export const fetchDashboardData = createAsyncThunk(
  "dashboard/fetchDashboardData",
  async (cityObj, { rejectWithValue }) => {
    try {
      const { name } = cityObj;
      
      // Refresh data and wait for completion
      await trafficApi.refreshData(name);
      
      // Fetch updated data in parallel
      const { summary, history } = await trafficApi.fetchDashboardData(name);
      
      return { summary, history };
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

// Optional: Separate thunk for just refreshing data without fetching
export const refreshCityData = createAsyncThunk(
  "dashboard/refreshCityData",
  async (cityName, { rejectWithValue }) => {
    try {
      return await trafficApi.refreshData(cityName);
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);