
import React, { useEffect, useMemo, useState } from "react";
import {
  AbsoluteFill,
  Easing,
  continueRender,
  delayRender,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { Text } from "@react-three/drei";
import {
  layoutTypography,
  type TypographyLayoutItem,
} from "./typographyLayout";

type Phrase = {
  id: string;
  text: string;
  fontSize: number;
  fontWeight: number;
  color: string;
  gapAfter?: number;
  z: number;
  rotationX: number;
  rotationY: number;
  rotationZ: number;
  emphasis?: boolean;
};

type TextMeasurement = {
  width: number;
  height: number;
};

const PHRASES: Phrase[] = [
  {
    id: "phrase-1",
    text: "In 1950,",
    fontSize: 0.85,
    fontWeight: 700,
    color: "#AE2225",
    gapAfter: 0.5,
    z: 0,
    rotationX: 0,
    rotationY: 0,
    rotationZ: 0,
  },
  {
    id: "phrase-2",
    text: "physicist Enrico Fermi",
    fontSize: 0.65,
    fontWeight: 600,
    color: "#202020",
    gapAfter: 0.4,
    z: -0.5,
    rotationX: 0.02,
    rotationY: -0.12,
    rotationZ: 0.015,
  },
  {
    id: "phrase-3",
    text: "posed a simple question",
    fontSize: 0.7,
    fontWeight: 700,
    color: "#AE2225",
    gapAfter: 0.8,
    z: -1,
    rotationX: -0.025,
    rotationY: 0.15,
    rotationZ: -0.012,
  },
  {
    id: "phrase-4",
    text: "about the universe.",
    fontSize: 0.75,
    fontWeight: 600,
    color: "#202020",
    z: -0.35,
    rotationX: 0,
    rotationY: -0.08,
    rotationZ: 0.01,
  },
];

const HOLD_FRAMES = 45;
const MOVE_FRAMES = [45, 105, 165, 225];

export const CameraWorld3dV2: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const [measurements, setMeasurements] = useState<
    Record<string, TextMeasurement>
  >({});

  const [renderHandle] = useState(() =>
    delayRender("Waiting for 3D typography measurements"),
  );

  const allMeasured = PHRASES.every(
    (phrase) => measurements[phrase.id] !== undefined,
  );

  useEffect(() => {
    if (allMeasured) {
      continueRender(renderHandle);
    }
  }, [allMeasured, renderHandle]);

  const positionedPhrases = useMemo(() => {
    const items: TypographyLayoutItem[] = PHRASES.map((phrase) => {
      const measured = measurements[phrase.id];

      return {
        id: phrase.id,
        width:
          measured?.width ??
          Math.max(0.5, phrase.text.length * phrase.fontSize * 0.45),
        height: measured?.height ?? phrase.fontSize,
        gapAfter: phrase.gapAfter,
      };
    });

    return layoutTypography(items);
  }, [measurements]);

  const positionById = useMemo(
    () => new Map(positionedPhrases.map((phrase) => [phrase.id, phrase])),
    [positionedPhrases],
  );

  // Hold the opening phrase completely still, then track the remaining phrases.
  const cameraX = interpolate(
  frame,
  [0, HOLD_FRAMES, 105, 165, 225],
  [
    positionedPhrases[0]?.x ?? 0,
    positionedPhrases[0]?.x ?? 0,
    positionedPhrases[1]?.x ?? 0,
    positionedPhrases[2]?.x ?? 0,
    positionedPhrases[3]?.x ?? 0,
  ],
  {
    easing: Easing.inOut(Easing.ease),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  },
);
  // Keep the opening view level, then gently introduce a camera-like rotation.
  const rotationY = interpolate(
    frame,
    [0, HOLD_FRAMES, 105, 165, 225],
    [0, 0, -0.025, 0.035, 0],
    {
      easing: Easing.inOut(Easing.ease),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const rotationX = interpolate(
    frame,
    [0, HOLD_FRAMES, 135, 225],
    [0, 0, 0.018, 0],
    {
      easing: Easing.inOut(Easing.ease),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#FBFAEA",
        fontFamily: "Georgia",
        fontStyle: "oblique",
        textAlign: "start"
      }}
    >
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 0, 12], fov: 40 }}
        style={{ backgroundColor: "#FBFAEA" }}
      >
        <ambientLight intensity={1} />

        <group
          position={[-cameraX, 0, 0]}
          rotation={[rotationX, rotationY, 0]}
        >
          {PHRASES.map((phrase) => {
            const position = positionById.get(phrase.id);

            return (
              <Text
                key={phrase.id}
                position={[
                  position?.x ?? 0,
                  position?.y ?? 0,
                  phrase.z,
                ]}
                rotation={[
                  phrase.rotationX,
                  phrase.rotationY,
                  phrase.rotationZ,
                ]}
                fontSize={phrase.fontSize}
                fontWeight={phrase.fontWeight}
                color={phrase.color}
                anchorX="center"
                anchorY="middle"
                textAlign="center"
                onSync={(mesh) => {
                  const textInfo = (
                    mesh as unknown as {
                      textRenderInfo?: {
                        blockBounds?: ArrayLike<number>;
                        visibleBounds?: ArrayLike<number>;
                      };
                    }
                  ).textRenderInfo;

                  const bounds =
                    textInfo?.blockBounds ?? textInfo?.visibleBounds;

                  if (!bounds || bounds.length < 4) return;

                  const next = {
                    width: Math.max(0.01, bounds[2] - bounds[0]),
                    height: Math.max(0.01, bounds[3] - bounds[1]),
                  };

                  setMeasurements((previous) => {
                    const old = previous[phrase.id];

                    if (
                      old &&
                      Math.abs(old.width - next.width) < 0.001 &&
                      Math.abs(old.height - next.height) < 0.001
                    ) {
                      return previous;
                    }

                    return { ...previous, [phrase.id]: next };
                  });
                }}
              >
                {phrase.text}
              </Text>
            );
          })}
        </group>
      </ThreeCanvas>
    </AbsoluteFill>
  );
};

