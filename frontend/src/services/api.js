import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const predictHeartDisease = (data) =>
  API.post("/predict", data);

export const getDanhSachBenhNhan = () =>
  API.get("/benh-nhan");

export const getLichSu = () =>
  API.get("/lich-su");

export const getThongKe = () =>
  API.get("/thong-ke");