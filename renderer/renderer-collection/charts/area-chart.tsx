import React from "react";
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type AreaChartData = {
  x: string | number;
  y: number;
};

export type AreaChartProps = {
  title: string;
  subtitle?: string;
  xTitle: string;
  yTitle: string;
  data: AreaChartData[];
};

const WIDTH = 1600;
const HEIGHT = 750;

const MARGIN = {
  top: 20,
  right: 30,
  bottom: 90,
  left: 100,
};

const GRID_COUNT = 5;

export const AreaChart: React.FC<AreaChartProps> = ({
  title,
  subtitle,
  xTitle,
  yTitle,
  data,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (data.length === 0) {
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
        }}
      >
        <div
          style={{
            fontSize: 42,
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
              color: "#737373",
            }}
          >
            {subtitle}
          </div>
        )}
      </div>
    );
  }

  const plotWidth = WIDTH - MARGIN.left - MARGIN.right;
  const plotHeight = HEIGHT - MARGIN.top - MARGIN.bottom;

  /*
   * ------------------------------------------------------------
   * Y scale
   * ------------------------------------------------------------
   */

  const rawMin = Math.min(...data.map((point) => point.y));
  const rawMax = Math.max(...data.map((point) => point.y));

  const rawRange = rawMax - rawMin || 1;

  const yMin = rawMin - rawRange * 0.08;
  const yMax = rawMax + rawRange * 0.08;

  const xPosition = (index: number) => {
    if (data.length === 1) {
      return MARGIN.left + plotWidth / 2;
    }

    return (
      MARGIN.left +
      (index / (data.length - 1)) * plotWidth
    );
  };

  const yPosition = (value: number) => {
    const normalized =
      (value - yMin) / (yMax - yMin);

    return (
      MARGIN.top +
      (1 - normalized) * plotHeight
    );
  };

  /*
   * ------------------------------------------------------------
   * Points
   * ------------------------------------------------------------
   */

  const points = data.map((point, index) => ({
    x: xPosition(index),
    y: yPosition(point.y),
    value: point.y,
    label: point.x,
  }));

  /*
   * ------------------------------------------------------------
   * Line path
   * ------------------------------------------------------------
   */

  const linePath = points
    .map((point, index) => {
      return `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`;
    })
    .join(" ");

  /*
   * ------------------------------------------------------------
   * Area path
   *
   * Start at the first data point,
   * follow the data line,
   * then return along the baseline.
   * ------------------------------------------------------------
   */

  const baselineY = MARGIN.top + plotHeight;

  const firstPoint = points[0];
  const lastPoint = points[points.length - 1];

  const areaPath = [
    `M ${firstPoint.x} ${baselineY}`,
    `L ${firstPoint.x} ${firstPoint.y}`,

    ...points
      .slice(1)
      .map(
        (point) =>
          `L ${point.x} ${point.y}`,
      ),

    `L ${lastPoint.x} ${baselineY}`,
    "Z",
  ].join(" ");

  /*
   * ------------------------------------------------------------
   * Animation
   * ------------------------------------------------------------
   *
   * 0 → 18
   * Grid reveals left → right
   *
   * 8 → 24
   * Axes appear
   *
   * 18 → 72
   * Area + line reveal left → right
   *
   * 55+
   * Points appear
   * ------------------------------------------------------------
   */

  const gridProgress = interpolate(
    frame,
    [0, 18],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const axisProgress = spring({
    frame: frame - 8,
    fps,
    config: {
      damping: 200,
      stiffness: 120,
    },
  });

  const areaProgress = interpolate(
    frame,
    [18, 72],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const pointProgress = spring({
    frame: frame - 58,
    fps,
    config: {
      damping: 180,
      stiffness: 140,
    },
  });

  /*
   * ------------------------------------------------------------
   * Grid values
   * ------------------------------------------------------------
   */

  const gridValues = Array.from(
    { length: GRID_COUNT },
    (_, index) => {
      return (
        yMax -
        ((yMax - yMin) * index) /
          (GRID_COUNT - 1)
      );
    },
  );

  /*
   * ------------------------------------------------------------
   * Unique SVG IDs
   *
   * Important because multiple AreaCharts may exist
   * in the same Remotion composition.
   * ------------------------------------------------------------
   */

  const chartId = `area-chart-${title
    .replace(/[^a-zA-Z0-9]/g, "")
    .toLowerCase()}`;

  const gridClipId = `${chartId}-grid`;
  const areaClipId = `${chartId}-area`;
  const gradientId = `${chartId}-gradient`;

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
      {/* ------------------------------------------------------ */}
      {/* Header */}
      {/* ------------------------------------------------------ */}

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

      {/* ------------------------------------------------------ */}
      {/* Chart */}
      {/* ------------------------------------------------------ */}

      <div
        style={{
          flex: 1,
          minHeight: 0,
          width: "100%",
        }}
      >
        <svg
          viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
          width="100%"
          height="100%"
          preserveAspectRatio="xMidYMid meet"
          style={{
            display: "block",
            overflow: "visible",
          }}
        >
          <defs>
            {/* ------------------------------------------------ */}
            {/* Grid reveal */}
            {/* ------------------------------------------------ */}

            <clipPath id={gridClipId}>
              <rect
                x={MARGIN.left}
                y={MARGIN.top}
                width={plotWidth * gridProgress}
                height={plotHeight}
              />
            </clipPath>

            {/* ------------------------------------------------ */}
            {/* Area reveal */}
            {/* ------------------------------------------------ */}

            <clipPath id={areaClipId}>
              <rect
                x={MARGIN.left}
                y={MARGIN.top}
                width={plotWidth * areaProgress}
                height={plotHeight}
              />
            </clipPath>

            {/* ------------------------------------------------ */}
            {/* Area gradient */}
            {/* ------------------------------------------------ */}

            <linearGradient
              id={gradientId}
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >
              <stop
                offset="0%"
                stopColor="#2563eb"
                stopOpacity={0.28}
              />

              <stop
                offset="100%"
                stopColor="#2563eb"
                stopOpacity={0.03}
              />
            </linearGradient>
          </defs>

          {/* -------------------------------------------------- */}
          {/* Grid */}
          {/* -------------------------------------------------- */}

          <g
            clipPath={`url(#${gridClipId})`}
            opacity={0.95}
          >
            {gridValues.map((value, index) => {
              const y = yPosition(value);

              return (
                <line
                  key={`grid-${index}`}
                  x1={MARGIN.left}
                  x2={MARGIN.left + plotWidth}
                  y1={y}
                  y2={y}
                  stroke="#e5e5e5"
                  strokeWidth={1}
                />
              );
            })}
          </g>

          {/* -------------------------------------------------- */}
          {/* Y-axis */}
          {/* -------------------------------------------------- */}

          <g opacity={axisProgress}>
            <line
              x1={MARGIN.left}
              x2={MARGIN.left}
              y1={MARGIN.top}
              y2={MARGIN.top + plotHeight}
              stroke="#d4d4d4"
              strokeWidth={1}
            />

            {gridValues.map((value, index) => {
              const y = yPosition(value);

              return (
                <text
                  key={`y-label-${index}`}
                  x={MARGIN.left - 18}
                  y={y}
                  textAnchor="end"
                  dominantBaseline="middle"
                  fill="#525252"
                  fontSize={16}
                  fontWeight={400}
                >
                  {Number.isInteger(value)
                    ? value
                    : value.toFixed(1)}
                </text>
              );
            })}

            {/* Y-axis title */}

            <text
              x={25}
              y={
                MARGIN.top +
                plotHeight / 2
              }
              textAnchor="middle"
              fill="#404040"
              fontSize={17}
              fontWeight={400}
              transform={`rotate(-90 25 ${
                MARGIN.top +
                plotHeight / 2
              })`}
            >
              {yTitle}
            </text>
          </g>

          {/* -------------------------------------------------- */}
          {/* X-axis */}
          {/* -------------------------------------------------- */}

          <g opacity={axisProgress}>
            <line
              x1={MARGIN.left}
              x2={MARGIN.left + plotWidth}
              y1={baselineY}
              y2={baselineY}
              stroke="#d4d4d4"
              strokeWidth={1}
            />

            {points.map((point, index) => {
              return (
                <text
                  key={`x-label-${index}`}
                  x={point.x}
                  y={baselineY + 28}
                  textAnchor="middle"
                  fill="#525252"
                  fontSize={16}
                  fontWeight={400}
                >
                  {point.label}
                </text>
              );
            })}

            {/* X-axis title */}

            <text
              x={
                MARGIN.left +
                plotWidth / 2
              }
              y={HEIGHT - 12}
              textAnchor="middle"
              fill="#404040"
              fontSize={17}
              fontWeight={400}
            >
              {xTitle}
            </text>
          </g>

          {/* -------------------------------------------------- */}
          {/* Area */}
          {/* -------------------------------------------------- */}

          <g
            clipPath={`url(#${areaClipId})`}
          >
            <path
              d={areaPath}
              fill={`url(#${gradientId})`}
            />

            {/* ------------------------------------------------ */}
            {/* Line */}
            {/* ------------------------------------------------ */}

            <path
              d={linePath}
              fill="none"
              stroke="#2563eb"
              strokeWidth={4}
              strokeLinecap="round"
              strokeLinejoin="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={
                1 - areaProgress
              }
            />
          </g>

          {/* -------------------------------------------------- */}
          {/* Data points */}
          {/* -------------------------------------------------- */}

          <g>
            {points.map((point, index) => {
              const pointDelay = index * 2;

              const opacity = spring({
                frame:
                  frame -
                  54 -
                  pointDelay,
                fps,
                config: {
                  damping: 180,
                  stiffness: 150,
                },
              });

              const scale = interpolate(
                opacity,
                [0, 1],
                [0.4, 1],
                {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                },
              );

              return (
                <g
                  key={`point-${index}`}
                  opacity={
                    opacity * pointProgress
                  }
                  transform={`translate(${point.x} ${point.y}) scale(${scale})`}
                >
                  <circle
                    r={7}
                    fill=""
                    stroke=""
                    strokeWidth={3}
                  />
                </g>
              );
            })}
          </g>
        </svg>
      </div>
    </div>
  );
};
