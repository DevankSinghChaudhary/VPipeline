import React from "react";
import {TypographyScene} from "../templates/TypographyScene";
import type {SceneData} from "../data/types";

export const SceneRenderer: React.FC<{scene: SceneData}> = ({scene}) => {
  if (scene.type !== "TYPOGRAPHY") {
    throw new Error(`Base renderer only supports TYPOGRAPHY; got ${scene.type}`);
  }

  return <TypographyScene scene={scene} />;
};
