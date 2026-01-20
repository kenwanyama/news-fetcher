import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

const TrendsChart = ({ trends }) => {
  const topicData = Object.entries(trends.topic_counts || {}).map(([key, value]) => ({ name: key, count: value }));
  const sentimentData = Object.entries(trends.sentiment_counts || {}).map(([key, value]) => ({ name: key, count: value }));

  return (
    <div>
      <h2>Article Trends</h2>
      <h3>Topics</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={topicData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>

      <h3>Sentiments</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={sentimentData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendsChart;
