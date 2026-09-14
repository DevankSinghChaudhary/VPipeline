import React from "react";
import {interpolate, useCurrentFrame, useVideoConfig} from "remotion";
import {Background} from "../components/Background";
import {TexturedText} from "../components/TexturedText";
import {TYPOGRAPHY} from "../design/typography";
import type {SceneData} from "../data/types";

export const TypographyScene: React.FC<{scene: SceneData}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const entranceFrames = Math.round(0.35 * fps);

  const opacity = interpolate(frame, [0, entranceFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, entranceFrames], [32, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const style = TYPOGRAPHY[scene.typography.type];

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      <Background />

      <div
        style={{
          position: "relative",
          zIndex: 1,
          width: "100%",
          padding: "0 120px",
          display: "flex",
          justifyContent: "center",
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        <TexturedText
          text={scene.typography.text}
          color={style.color}
        />
      </div>
    </div>
  );
};
