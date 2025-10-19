import { createSlice } from "@reduxjs/toolkit";
import { fetchDashboardData, refreshCityData } from "./dashboardThunks";

const initialState = {
  city: null,
  summary: {},
  history: [],
  loading: false,
  refreshing: false,
  lastUpdated: null,
  error: null,
};

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState,
  reducers: {
    setCity: (state, action) => {
      state.city = action.payload;
      state.error = null; // Clear error when city changes
    },
    clearError: (state) => {
      state.error = null;
    },
    clearData: (state) => {
      state.summary = {};
      state.history = [];
      state.lastUpdated = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Main dashboard data fetch
      .addCase(fetchDashboardData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.loading = false;
        state.summary = action.payload.summary || {};
        state.history = action.payload.history || [];
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Separate refresh action
      .addCase(refreshCityData.pending, (state) => {
        state.refreshing = true;
      })
      .addCase(refreshCityData.fulfilled, (state) => {
        state.refreshing = false;
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(refreshCityData.rejected, (state, action) => {
        state.refreshing = false;
        state.error = action.payload;
      });
  },
});

export const { setCity, clearError, clearData } = dashboardSlice.actions;
export default dashboardSlice.reducer;