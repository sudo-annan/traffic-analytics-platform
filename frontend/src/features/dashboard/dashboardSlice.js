// src/features/dashboard/dashboardSlice.js
import { createSlice } from "@reduxjs/toolkit";
import { fetchDashboardData } from "./dashboardThunks";

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState: {
    city: null, // stores { name, lat, lon }
    summary: {},
    history: [],
    loading: false,
  },
  reducers: {
    setCity: (state, action) => {
      state.city = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardData.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.loading = false;
        state.summary = action.payload.summary || {};
        state.history = action.payload.history || [];
      })
      .addCase(fetchDashboardData.rejected, (state) => {
        state.loading = false;
      });
  },
});

export const { setCity } = dashboardSlice.actions;
export default dashboardSlice.reducer;
