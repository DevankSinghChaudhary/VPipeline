
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
  font?: string;
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
  },
  {
    id: "phrase-2",
    text: "physicist Enrico Fermi",
    fontSize: 0.65,
    fontWeight: 600,
    color: "#202020",
    gapAfter: 0.4,
  },
  {
    id: "phrase-3",
    text: "posed a simple question",
    fontSize: 0.7,
    fontWeight: 700,
    color: "#AE2225",
    gapAfter: 0.8,
  },
  {
    id: "phrase-4",
    text: "about the universe.",
    fontSize: 0.75,
    fontWeight: 600,
    color: "#202020",
  },
];

export const CameraWorld3d: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const [measurements, setMeasurements] = useState<
    Record<string, TextMeasurement>
  >({});

  const [renderHandle] = useState(() =>
    delayRender("Waiting for typography measurements"),
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
      const measurement = measurements[phrase.id];

      return {
        id: phrase.id,
        width:
          measurement?.width ??
          Math.max(0.5, phrase.text.length * phrase.fontSize * 0.45),
        height: measurement?.height ?? phrase.fontSize,
        gapAfter: phrase.gapAfter,
      };
    });

    return layoutTypography(items);
  }, [measurements]);

  const cameraTargets = positionedPhrases.map((phrase) => phrase.x);

  const cameraX = interpolate(
    frame,
    [0, 60, 120, 180],
    cameraTargets,
    {
      easing: Easing.inOut(Easing.ease),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const positionById = new Map(
    positionedPhrases.map((phrase) => [phrase.id, phrase]),
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#FBFAEA" }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [0, 0, 12], fov: 40 }}
        style={{ backgroundColor: "#FBFAEA" }}
      >
        <ambientLight intensity={1} />

        <group position={[-cameraX, 0, 0]}>
          {PHRASES.map((phrase) => {
            const position = positionById.get(phrase.id);

            return (
              <Text
                key={phrase.id}
                position={[
                  position?.x ?? 0,
                  position?.y ?? 0,
                  0,
                ]}
                fontSize={phrase.fontSize}
                fontWeight={phrase.fontWeight}
                font={phrase.font}
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

                  if (!bounds || bounds.length < 4) {
                    return;
                  }

                  const nextMeasurement = {
                    width: Math.max(
                      0.01,
                      bounds[2] - bounds[0],
                    ),
                    height: Math.max(
                      0.01,
                      bounds[3] - bounds[1],
                    ),
                  };

                  setMeasurements((previous) => {
                    const old = previous[phrase.id];

                    if (
                      old &&
                      Math.abs(
                        old.width - nextMeasurement.width,
                      ) < 0.001 &&
                      Math.abs(
                        old.height - nextMeasurement.height,
                      ) < 0.001
                    ) {
                      return previous;
                    }

                    return {
                      ...previous,
                      [phrase.id]: nextMeasurement,
                    };
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

