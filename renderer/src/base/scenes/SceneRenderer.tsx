import React from "react";
import type { ManifestScene } from "../data/types";
import { ImageScene } from "../../image/ImageScene";
import { ImageWithTextScene } from "../../image_with_text/ImageWithTextScene";
import { TypographyScene } from "../../typography/TypographyScene";
import { NoneScene } from "../../none/NoneScene";

interface SceneRendererProps {
  scene: ManifestScene;
}

export const SceneRenderer: React.FC<SceneRendererProps> = ({ scene }) => {
  switch (scene.type) {
    case "IMAGE":
      return <ImageScene scene={scene} />;
    case "IMAGE_WITH_TEXT":
      return <ImageWithTextScene scene={scene} />;
    case "TYPOGRAPHY":
      return <TypographyScene scene={scene} />;
    case "NONE":
      return <NoneScene scene={scene} />;
    default:
      throw new Error(`Unsupported scene type: ${scene.type}`);
  }
};
