import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import type { ManifestScene } from "../base/data/types";

interface Props {
  scene: ManifestScene;
}

export const ImageWithTextScene: React.FC<Props> = ({ scene }) => {
  const image = scene.visual.image?.[0];
  const text = scene.visual.text ?? "";

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {image && (
        <Img
          src={staticFile(image)}
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      )}

      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "rgba(0, 0, 0, 0.35)",
        }}
      >
        <div
          style={{
            color: "white",
            fontSize: 120,
            fontWeight: 800,
            textAlign: "center",
          }}
        >
          {text}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
