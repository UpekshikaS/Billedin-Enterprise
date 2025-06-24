import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000", // Your Flask backend
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
