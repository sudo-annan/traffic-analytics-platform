// src/features/dashboard/dashboardThunks.js
import { createAsyncThunk } from "@reduxjs/toolkit";
import { refreshData, fetchSummary, fetchHistory } from "../../api/trafficApi";

export const fetchDashboardData = createAsyncThunk(
  "dashboard/fetchDashboardData",
  async (cityObj, { rejectWithValue }) => {
    try {
      const { name, lat, lon } = cityObj;
      await refreshData(name, lat, lon); // trigger extract + ETL
      const summary = await fetchSummary(name);
      const history = await fetchHistory(name);
      return { summary, history };
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);
