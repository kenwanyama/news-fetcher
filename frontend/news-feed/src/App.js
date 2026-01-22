import React, { useEffect, useState } from "react";
import { fetchArticles, fetchTrends } from "./api";
import ArticleList from "./components/ArticleList";
import TrendsChart from "./components/TrendsChart";

function App() {
  const [articles, setArticles] = useState([]);
  const [trends, setTrends] = useState({});
  const [activeTopic, setActiveTopic] = useState("ALL");

  useEffect(() => {
    const getData = async () => {
      const articlesData = await fetchArticles();
      setArticles(articlesData);
      const trendsData = await fetchTrends();
      setTrends(trendsData);
    };
    getData();
  }, []);

  const topics = ["ALL", ...new Set(articles.map(a => a.topic))];

  return (
    <div className="app-container">
      <h1 className="app-title">Brief.ly</h1>
      <p className="subtitle">News at a glance</p>
      <TrendsChart trends={trends} />
      
      <div className="tabs">
        {topics.map(topic => (
          <button
            key={topic}
            className={`tab ${activeTopic === topic ? "active" : ""}`}
            onClick={() => setActiveTopic(topic)}
          >
            {topic}
          </button>
        ))}
      </div>

      <ArticleList articles={articles} activeTopic={activeTopic} />
    </div>
  );
}

export default App;
