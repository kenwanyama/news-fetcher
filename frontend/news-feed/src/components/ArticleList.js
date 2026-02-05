import React from "react";

const ArticleList = ({ articles, activeTopic }) => {
  const filteredArticles =
    activeTopic === "ALL"
      ? articles
      : articles.filter(a => a.topic === activeTopic);

  return (
    <div>
      {filteredArticles.map((article) => (
        <div key={article.id} className="article-card">
          <h3>{article.title}</h3>
          <p className="article-meta">
            [{article.source.toUpperCase()}] — TOPIC: {article.topic} — SENTIMENT:{" "}
            <span className={`sentiment ${article.sentiment.toLowerCase()}`}>
              {article.sentiment?.replace("LABEL_", "") || "Processing..."}
            </span>
          </p>
          <p className="article-summary">
            {article.generated_summary}
          </p>
          <a href={article.link} target="_blank" rel="noreferrer">
            Read full article →
          </a>
        </div>
      ))}
    </div>
  );
};

export default ArticleList;
