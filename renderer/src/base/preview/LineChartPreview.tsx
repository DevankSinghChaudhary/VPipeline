import React from "react";
import { LineChart } from "../../../renderer-collection/charts/line-chart";

const data = [
  { x: 1950, y: 2.5 },
  { x: 1960, y: 3.0 },
  { x: 1970, y: 3.7 },
  { x: 1980, y: 4.4 },
  { x: 1990, y: 6.2 },
  { x: 2000, y: 6.1 },
  { x: 2010, y: 6.9 },
  { x: 2020, y: 7.8 },
];

export const LineChartPreview = () => {
  return (
    <LineChart
      title="Global Population"
      subtitle="Population growth from 1950 to 2020"
      xTitle="Year"
      yTitle="Population (billions)"
      data={data}
    />
  );
};

