import axios from "axios";

// The address of your FastAPI backend
const API_BASE = "http://localhost:8000";

// Get the list of cities
export const getCities = async () => {
  const res = await axios.get(`${API_BASE}/cities`);
  return res.data;
};

// Get the latest weather for one city
export const getWeather = async (city) => {
  const res = await axios.get(`${API_BASE}/weather/${city}`);
  return res.data;
};

// Get the history for one city
export const getHistory = async (city) => {
  const res = await axios.get(`${API_BASE}/weather/${city}/history`);
  return res.data;
};

