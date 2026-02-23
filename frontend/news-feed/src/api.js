import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "https://news-fetcher-production-e5bb.up.railway.app";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000, // 30 seconds timeout
});

export const fetchArticles = async () => {
  try {
    const res = await api.get("/articles");  
    return res.data;
  } catch (error) {
    console.error("Error fetching articles:", error);
    return [];
  }
};

export const fetchTrends = async () => {
  try {
    const res = await api.get("/articles/trends");  
    return res.data.topic_counts || {};
  } catch (error) {
    console.error("Error fetching trends:", error);
    return {};
  }
};
