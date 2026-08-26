import {useId} from "react";
import {colors} from "../design/colors";

type Props = {
  text: string;
  color?: keyof typeof colors;

  fontSize?: number;
  fontWeight?: number;
  letterSpacing?: number;
  fontFamily?: string;

  /* Printed ink */
  inkSpread?: number;
  inkSoftness?: number;

  /* Organic edge */
  roughness?: number;
  roughnessScale?: number;

  /* Grain */
  grain?: boolean;
  grainScale?: number;
  grainOpacity?: number;
  grainContrast?: number;

  /* Tone */
  brightness?: number;
  contrast?: number;
  gamma?: number;

  /* Chromatic aberration */
  chromaticAberration?: boolean;
  chromaticOffset?: number;
  chromaticOpacity?: number;
};

export const TexturedText = ({
  text,
  color = "primary",

  fontSize = 79,
  fontWeight = 450,
  letterSpacing = -0.02,
  fontFamily = "inherit",

  inkSpread = 1,
  inkSoftness = 0,

  roughness = 0.8,
  roughnessScale = 0.01,

  grain = true,
  grainScale = 0.3,
  grainOpacity = 0.12,
  grainContrast = 1.6,

  brightness = 0,
  contrast = 1,
  gamma = 1,

  chromaticAberration = true,
  chromaticOffset = 1.9,
  chromaticOpacity = 0.5,
}: Props) => {
  const id = useId().replace(/:/g, "");

  const inkFilterId = `ink-${id}`;
  const grainFilterId = `grain-${id}`;
  const toneFilterId = `tone-${id}`;

  const grainMaskId = `grain-mask-${id}`;

  const width = Math.max(
    text.length * fontSize * 0.65,
    fontSize,
  );

  const height = fontSize * 1.4;

  /*
   * SVG color values are easier to manipulate when we
   * use the original color for the main layer and
   * simple RGB colors for the aberration layers.
   */

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{
        display: "block",
        overflow: "visible",
      }}
    >
      <defs>

        {/* =====================================================
            INK / PRINT FILTER
           ===================================================== */}

        <filter
          id={inkFilterId}
          x="-15%"
          y="-20%"
          width="130%"
          height="140%"
          colorInterpolationFilters="sRGB"
        >
          {/* Soften digital font edge */}
          <feGaussianBlur
            in="dilate"
            stdDeviation={inkSoftness}
            result="soft"
          />

          {/* Spread ink */}
          <feMorphology
            in="soft"
            operator="dilate"
            radius={inkSpread}
            result="spread"
          />

          {/* Large organic variation */}
          <feTurbulence
            type="fractalNoise"
            baseFrequency={roughnessScale}
            numOctaves="2"
            seed="17"
            result="edgeNoise"
          />

          {/* Organic ink boundary */}
          <feDisplacementMap
            in="spread"
            in2="edgeNoise"
            scale={roughness}
            xChannelSelector="R"
            yChannelSelector="G"
            result="organic"
          />

          {/* Final tiny softening */}
          <feGaussianBlur
            in="organic"
            stdDeviation="0.12"
          />
        </filter>

        {/* =====================================================
            GRAIN
           ===================================================== */}

        <filter
          id={grainFilterId}
          x="-20%"
          y="-20%"
          width="140%"
          height="140%"
          colorInterpolationFilters="sRGB"
        >
          <feTurbulence
            type="fractalNoise"
            baseFrequency={grainScale}
            numOctaves="3"
            seed="42"
            result="grain"
          />

          {/* Grayscale */}
          <feColorMatrix
            in="grain"
            type="saturate"
            values="0"
            result="gray"
          />

          {/* Grain contrast */}
          <feComponentTransfer>
            <feFuncR
              type="linear"
              slope={grainContrast}
            />

            <feFuncG
              type="linear"
              slope={grainContrast}
            />

            <feFuncB
              type="linear"
              slope={grainContrast}
            />
          </feComponentTransfer>
        </filter>

        {/* =====================================================
            TONE / CURVES-LIKE CONTROL
           ===================================================== */}

        <filter
          id={toneFilterId}
          x="-10%"
          y="-10%"
          width="120%"
          height="120%"
          colorInterpolationFilters="sRGB"
        >
          <feComponentTransfer>
            <feFuncR
              type="gamma"
              amplitude={1 + brightness}
              exponent={gamma}
              offset={0}
            />

            <feFuncG
              type="gamma"
              amplitude={1 + brightness}
              exponent={gamma}
              offset={0}
            />

            <feFuncB
              type="gamma"
              amplitude={1 + brightness}
              exponent={gamma}
              offset={0}
            />

            <feFuncA
              type="linear"
              slope={contrast}
            />
          </feComponentTransfer>
        </filter>

        {/* =====================================================
            GRAIN MASK
           ===================================================== */}

        <mask id={grainMaskId}>
          <text
            x="0"
            y={fontSize}
            fill="white"
            fontSize={fontSize}
            fontWeight={fontWeight}
            fontFamily={fontFamily}
            letterSpacing={`${letterSpacing}em`}
            filter={`url(#${inkFilterId})`}
          >
            {text}
          </text>
        </mask>
      </defs>

      {/* =====================================================
          CHROMATIC ABERRATION
         ===================================================== */}

      {chromaticAberration && (
        <>
          {/* Red fringe */}
          <text
            x={-chromaticOffset}
            y={fontSize}
            fill="#ff0000"
            opacity={chromaticOpacity}
            fontSize={fontSize}
            fontWeight={fontWeight}
            fontFamily={fontFamily}
            letterSpacing={`${letterSpacing}em`}
            filter={`url(#${inkFilterId})`}
          >
            {text}
          </text>

          {/* Blue fringe */}
          <text
            x={chromaticOffset}
            y={fontSize}
            fill="#00aaff"
            opacity={chromaticOpacity}
            fontSize={fontSize}
            fontWeight={fontWeight}
            fontFamily={fontFamily}
            letterSpacing={`${letterSpacing}em`}
            filter={`url(#${inkFilterId})`}
          >
            {text}
          </text>
        </>
      )}

      {/* =====================================================
          MAIN TEXT
         ===================================================== */}

      <text
        x="0"
        y={fontSize}
        fill={colors[color]}
        fontSize={fontSize}
        fontWeight={fontWeight}
        fontFamily={fontFamily}
        letterSpacing={`${letterSpacing}em`}
        filter={`url(#${inkFilterId})`}
      >
        {text}
      </text>

      {/* =====================================================
          PROCEDURAL GRAIN
         ===================================================== */}

      {grain && (
        <rect
          x="0"
          y="0"
          width={width}
          height={height}
          fill="white"
          opacity={grainOpacity}
          filter={`url(#${grainFilterId})`}
          mask={`url(#${grainMaskId})`}
          pointerEvents="none"
        />
      )}

      {/* =====================================================
          TONE OVERLAY
         ===================================================== */}

      {(brightness !== 0 ||
        contrast !== 1 ||
        gamma !== 1) && (
        <text
          x="0"
          y={fontSize}
          fill={colors[color]}
          opacity={0.001}
          fontSize={fontSize}
          fontWeight={fontWeight}
          fontFamily={fontFamily}
          letterSpacing={`${letterSpacing}em`}
          filter={`url(#${toneFilterId})`}
        >
          {text}
        </text>
      )}
    </svg>
  );
};
