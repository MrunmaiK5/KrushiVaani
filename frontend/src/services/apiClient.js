import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000", // Your FastAPI backend
});

export default apiClient;