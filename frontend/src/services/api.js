import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getHistory = async () => {
  const response = await API.get("/history");
  return response;
};

export const predictHeartDisease = async (payload) => {
  const response = await API.post("/predict", payload);
  return response;
};