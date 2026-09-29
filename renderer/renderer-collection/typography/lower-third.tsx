import React from "react";
import {
  Easing,
  interpolate,
  useCurrentFrame,
} from "remotion";

export type LowerThirdProps = {
  /**
   * Main text / person's name.
   */
  main: string;

  /**
   * Secondary text / designation.
   */
  subtitle: string;

  /**
   * Background image.
   * Can be a public/Remotion static file path.
   */
  image: string;

  accentColor?: string;
  mainColor?: string;
  subtitleColor?: string;

  mainFontSize?: number;
  subtitleFontSize?: number;

  fontFamily?: string;

  /**
   * Lower-third animation duration.
   */
  durationInFrames?: number;

  /**
   * Delay before the lower-third animation starts.
   */
  delayInFrames?: number;

  /**
   * Starting image scale.
   */
  imageStartScale?: number;

  /**
   * Ending image scale.
   */
  imageEndScale?: number;

  /**
   * Duration of the image zoom.
   *
   * This is intentionally independent from the
   * lower-third animation.
   */
  imageZoomDurationInFrames?: number;

  /**
   * Image positioning.
   */
  imageObjectPosition?: string;
};

export const LowerThird: React.FC<LowerThirdProps> = ({
  main,
  subtitle,
  image,

  accentColor = "#000000",
  mainColor = "#070707",
  subtitleColor = "#070707",

  mainFontSize = 42,
  subtitleFontSize = 24,

  fontFamily = "Inter, Arial, Helvetica, sans-serif",

  durationInFrames = 50,
  delayInFrames = 0,

  imageStartScale = 1,
  imageEndScale = 1.06,
  imageZoomDurationInFrames = 180,

  imageObjectPosition = "center",
}) => {
  const frame = useCurrentFrame();

  /*
   * ---------------------------------------------------------
   * LAYOUT
   * ---------------------------------------------------------
   */

  const accentWidth = 2;

  const mainX = 15;
  const subtitleX = 15;

  const mainY = 48;
  const subtitleY = 80;

  const estimatedMainWidth = Math.max(
    100,
    main.length * mainFontSize * 0.55,
  );

  const estimatedSubtitleWidth = Math.max(
    100,
    subtitle.length * subtitleFontSize * 0.55,
  );

  const totalWidth =
    Math.max(
      estimatedMainWidth,
      estimatedSubtitleWidth,
    ) + 70;

  const totalHeight = 100;

  /*
   * ---------------------------------------------------------
   * TIMELINE
   * ---------------------------------------------------------
   */

  const localFrame = Math.max(
    0,
    frame - delayInFrames,
  );

  /*
   * ---------------------------------------------------------
   * ACCENT LINE — ENTRANCE
   * ---------------------------------------------------------
   */

  const accentProgress = interpolate(
    localFrame,
    [0, 10],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    },
  );

  /*
   * ---------------------------------------------------------
   * MAIN TEXT — ENTRANCE
   * ---------------------------------------------------------
   */

  const mainProgress = interpolate(
    localFrame,
    [7, 20],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    },
  );

  /*
   * ---------------------------------------------------------
   * SUBTITLE — ENTRANCE
   * ---------------------------------------------------------
   */

  const subtitleProgress = interpolate(
    localFrame,
    [14, 30],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    },
  );

  /*
   * ---------------------------------------------------------
   * EXIT
   * ---------------------------------------------------------
   *
   * The lower third holds fully visible first.
   *
   * Only near the end does the accent line collapse.
   * The text itself does not independently animate away.
   *
   * Because the text is revealed from the accent line,
   * collapsing the line/reveal effectively removes the
   * complete lower third.
   */

  const exitStart = durationInFrames - 10;

  const exitProgress = interpolate(
    localFrame,
    [exitStart, durationInFrames],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.in(Easing.cubic),
    },
  );

  /*
   * ---------------------------------------------------------
   * IMAGE ANIMATION
   * ---------------------------------------------------------
   *
   * Completely independent from the lower-third animation.
   */

  const imageScale = interpolate(
    frame,
    [0, imageZoomDurationInFrames],
    [imageStartScale, imageEndScale],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.linear,
    },
  );

  /*
   * ---------------------------------------------------------
   * TEXT MOTION
   * ---------------------------------------------------------
   *
   * Entrance only.
   *
   * There is deliberately NO exit translation.
   */

  const mainTranslateX = interpolate(
    mainProgress,
    [0, 1],
    [-18, 0],
  );

  const subtitleTranslateX = interpolate(
    subtitleProgress,
    [0, 1],
    [-18, 0],
  );

  const mainTranslateY = interpolate(
    mainProgress,
    [0, 1],
    [3, 0],
  );

  const subtitleTranslateY = interpolate(
    subtitleProgress,
    [0, 1],
    [3, 0],
  );

  /*
   * ---------------------------------------------------------
   * EXIT REVEAL
   * ---------------------------------------------------------
   *
   * During the hold:
   *
   *   0 → full text
   *
   * During exit:
   *
   *   full text → nothing
   *
   * The text itself doesn't move.
   * The visible region simply collapses.
   */

  const exitRevealProgress =
    exitProgress > 0
      ? 1 - exitProgress
      : 1;

  const mainClipWidth =
    estimatedMainWidth *
    mainProgress *
    exitRevealProgress;

  const subtitleClipWidth =
    estimatedSubtitleWidth *
    subtitleProgress *
    exitRevealProgress;

  /*
   * Accent line:
   *
   * entrance: 0 → 85
   * hold:     85
   * exit:     85 → 0
   */

  const accentHeight =
    exitProgress > 0
      ? interpolate(
          exitProgress,
          [0, 1],
          [85, 0],
        )
      : 85 * accentProgress;

  /*
   * ---------------------------------------------------------
   * RENDER
   * ---------------------------------------------------------
   */

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        overflow: "hidden",
      }}
    >
      {/* =====================================================
          BACKGROUND IMAGE
          ===================================================== */}

      <img
        src={image}
        style={{
          position: "absolute",
          inset: 0,

          width: "100%",
          height: "100%",

          objectFit: "cover",
          objectPosition: imageObjectPosition,

          transform: `scale(${imageScale})`,
          transformOrigin: "center center",

          zIndex: 0,
        }}
      />

      {/* =====================================================
          LOWER THIRD
          ===================================================== */}

      <div
        style={{
          position: "absolute",
          left: 100,
          bottom: 100,
          zIndex: 1,
        }}
      >
        <svg
          width={totalWidth}
          height={totalHeight}
          viewBox={`0 0 ${totalWidth} ${totalHeight}`}
          style={{
            display: "block",
            overflow: "visible",
            fontFamily,
          }}
        >
          <defs>
            {/* ---------------------------------------------
                MAIN TEXT MASK
                --------------------------------------------- */}

            <clipPath id="lower-third-main-clip">
              <rect
                x={mainX}
                y={0}
                width={mainClipWidth}
                height={mainFontSize + 15}
              />
            </clipPath>

            {/* ---------------------------------------------
                SUBTITLE MASK
                --------------------------------------------- */}

            <clipPath id="lower-third-subtitle-clip">
              <rect
                x={subtitleX}
                y={subtitleY - subtitleFontSize}
                width={subtitleClipWidth}
                height={subtitleFontSize + 15}
              />
            </clipPath>
          </defs>

          {/* =================================================
              ACCENT LINE
              ================================================= */}

          <rect
            x={0}
            y={8}
            width={accentWidth}
            height={accentHeight}
            rx={accentWidth / 2}
            fill={accentColor}
          />

          {/* =================================================
              MAIN / NAME
              ================================================= */}

          <g
            clipPath="url(#lower-third-main-clip)"
            transform={`
              translate(
                ${mainTranslateX}
                ${mainTranslateY}
              )
            `}
          >
            <text
              x={mainX}
              y={mainY}
              fill={mainColor}
              fontSize={mainFontSize}
              fontWeight={600}
              letterSpacing="-0.5"
            >
              {main}
            </text>
          </g>

          {/* =================================================
              SUBTITLE / DESIGNATION
              ================================================= */}

          <g
            clipPath="url(#lower-third-subtitle-clip)"
            transform={`
              translate(
                ${subtitleTranslateX}
                ${subtitleTranslateY}
              )
            `}
          >
            <text
              x={subtitleX}
              y={subtitleY}
              fill={subtitleColor}
              fontSize={subtitleFontSize}
              fontWeight={500}
            >
              {subtitle}
            </text>
          </g>
        </svg>
      </div>
    </div>
  );
};
