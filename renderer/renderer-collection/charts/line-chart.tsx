import React from "react";
import {
  CartesianGrid,
  Line,
  LineChart as RechartsLineChart,
  XAxis,
  YAxis,
} from "recharts";

export type LineChartData = {
  x: string | number;
  y: number;
};

export type LineChartProps = {
  title: string;
  subtitle?: string;
  xTitle: string;
  yTitle: string;
  data: LineChartData[];
};

export const LineChart: React.FC<LineChartProps> = ({
  title,
  subtitle,
  xTitle,
  yTitle,
  data,
}) => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#fafafa",
        color: "#171717",
        fontFamily: "Inter, Arial, sans-serif",
        boxSizing: "border-box",
        padding: "64px 72px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <div
        style={{
          marginBottom: 36,
        }}
      >
        <div
          style={{
            fontSize: 42,
            lineHeight: 1.1,
            fontWeight: 650,
            letterSpacing: "-0.025em",
          }}
        >
          {title}
        </div>

        {subtitle && (
          <div
            style={{
              marginTop: 10,
              fontSize: 20,
              lineHeight: 1.4,
              color: "#737373",
              fontWeight: 400,
            }}
          >
            {subtitle}
          </div>
        )}
      </div>

      {/* Chart */}
      <div
        style={{
          flex: 1,
          minHeight: 0,
        }}
      >
        <RechartsLineChart
          width={1600}
          height={750}
          data={data}
          margin={{
            top: 20,
            right: 30,
            bottom: 70,
            left: 90,
          }}
        >
          <CartesianGrid
            vertical={false}
            stroke="#e5e5e5"
            strokeWidth={1}
          />

          <XAxis
            dataKey="x"
            tickLine={false}
            axisLine={{
              stroke: "#d4d4d4",
            }}
            tick={{
              fill: "#525252",
              fontSize: 16,
            }}
            tickMargin={14}
            label={{
              value: xTitle,
              position: "insideBottom",
              offset: -45,
              fill: "#404040",
              fontSize: 17,
            }}
          />

          <YAxis
            dataKey="y"
            tickLine={false}
            axisLine={false}
            tick={{
              fill: "#525252",
              fontSize: 16,
            }}
            tickMargin={12}
            label={{
              value: yTitle,
              angle: -90,
              position: "insideLeft",
              offset: -55,
              fill: "#404040",
              fontSize: 17,
            }}
          />

          <Line
            type="monotone"
            dataKey="y"
            stroke="#2563eb"
            strokeWidth={4}
            dot={false}
            activeDot={false}
          />
        </RechartsLineChart>
      </div>
    </div>
  );
};
