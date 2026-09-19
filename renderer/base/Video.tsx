import React from "react";
import { Audio, staticFile, Solid } from "remotion";
import { TypographyScene } from "./templates/TypographyScene";
import type { SceneData } from "./data/types";

export type VideoProps = { scene: SceneData };

export const Video: React.FC<VideoProps> = ({ scene }) => (
  <>
    <Audio src={staticFile(scene.audio.path)} />
    <TypographyScene scene={scene} />
  </>
);
