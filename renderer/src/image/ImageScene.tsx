import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import type { ManifestScene } from "../base/data/types";

interface Props {
  scene: ManifestScene;
}

export const ImageScene: React.FC<Props> = ({ scene }) => {
  const image = scene.visual.image?.[0];

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {image && (
        <Img
          src={staticFile(image)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      )}
    </AbsoluteFill>
  );
};
