import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
} from "remotion";
import type { ManifestScene } from "../base/data/types";

interface Props {
  scene: ManifestScene;
}

export const TypographyScene: React.FC<Props> = ({ scene }) => {
  const frame = useCurrentFrame();
  const text = scene.visual.text ?? "";

  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#080808",
        alignItems: "center",
        justifyContent: "center",
        padding: 120,
      }}
    >
      <div
        style={{
          color: "white",
          fontSize: 90,
          fontWeight: 700,
          textAlign: "center",
          opacity,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
