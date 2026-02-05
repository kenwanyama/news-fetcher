import React from "react";
import { BarChart, Bar, XAxis, ResponsiveContainer } from "recharts";

const TrendsChart = ({ trends }) => {
  const topicData = Object.entries(trends || {}).map(([key, value]) => ({ name: key, count: value }));
 

  return (
 
    <div className="chart-box">
      <h3>TOPIC DISTRIBUTION</h3>
      <ResponsiveContainer width="80%" height={400}>
        <BarChart data={topicData}>
          <XAxis 
          dataKey="name" 
          tick={{ fontSize: 11 }}
          angle={-45}
          textAnchor="end"
          height={50}
        />
          <Bar dataKey="count" fill="#2e6f40" radius={0} />
        </BarChart>
      </ResponsiveContainer>
    </div>
);
};

export default TrendsChart;
