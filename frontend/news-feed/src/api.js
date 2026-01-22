import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export const fetchArticles = async () => {
  const res = await axios.get(`${API_BASE}/articles`);
  return res.data;
};

export const fetchTrends = async () => {
  const res = await axios.get(`${API_BASE}/articles/trends`);
  return res.data;
};
