import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

// Only fetch the summary
export const fetchTrafficSummary = createAsyncThunk(
  "traffic/fetchSummary",
  async () => {
    const response = await axios.get(`${API_BASE_URL}/api/v1/traffic/summary`);
    return response.data;
  }
);

export const fetchTrafficHistory = createAsyncThunk(
  "traffic/fetchHistory",
  async () => {
    const response = await axios.get(`${API_BASE_URL}/api/v1/traffic/history`);
    return response.data;
  }
);

const trafficSlice = createSlice({
  name: "traffic",
  initialState: {
    data: null,
    history: [],
    status: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTrafficSummary.fulfilled, (state, action) => {
        state.data = action.payload;
      })
      .addCase(fetchTrafficHistory.fulfilled, (state, action) => {
        state.history = action.payload;
      });
  },
});

export default trafficSlice.reducer;
