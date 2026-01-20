import React from "react";

const ArticleList = ({ articles }) => {
  return (
    <div>
      <h2>Latest Articles</h2>
      {articles.map((article) => (
        <div key={article.id} style={{ border: "1px solid #ddd", margin: "10px", padding: "10px" }}>
          <h3>{article.title}</h3>
          <p><strong>Source:</strong> {article.source}</p>
          <p><strong>Topic:</strong> {article.topic} | <strong>Sentiment:</strong> {article.sentiment}</p>
          <p>{article.generated_summary}</p>
          <a href={article.link} target="_blank" rel="noreferrer">Read full article</a>
        </div>
      ))}
    </div>
  );
};

export default ArticleList;
