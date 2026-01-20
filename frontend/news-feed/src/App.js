import React, { useEffect, useState } from "react";
import { fetchArticles, fetchTrends } from "./api";
import ArticleList from "./components/ArticleList";
import TrendsChart from "./components/TrendsChart";

function App() {
  const [articles, setArticles] = useState([]);
  const [trends, setTrends] = useState({});

  useEffect(() => {
    const getData = async () => {
      const articlesData = await fetchArticles();
      setArticles(articlesData);

      const trendsData = await fetchTrends();
      setTrends(trendsData);
    };
    getData();
  }, []);

  return (
    <div style={{ maxWidth: "900px", margin: "auto", padding: "20px" }}>
      <h1>Brief.ly</h1>
      <h2>News at a glance</h2>
      <TrendsChart trends={trends} />
      <ArticleList articles={articles} />
    </div>
  );
}

export default App;
