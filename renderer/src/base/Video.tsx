import React from "react";
import { AbsoluteFill, Sequence, Audio, staticFile } from "remotion";
import type { RendererManifest } from "./data/types";
import { DebugTypographyScene } from "../debug/DebugTypographyScene";

type Props = {
  manifest: RendererManifest;
};

const FPS = 30;

export const Video: React.FC<Props> = ({ manifest }) => {
  let startFrame = 0;

  return (
    <AbsoluteFill>
      <Audio src={staticFile("bgMusic/bg.mp3")} volume={0.1} />
      {manifest.map((scene) => {
        const durationInFrames = Math.ceil(scene.duration * FPS);
        const sceneStart = startFrame;

        startFrame += durationInFrames;

        return (
          <Sequence
            key={scene.scene_id}
            from={sceneStart}
            durationInFrames={durationInFrames}
          >
            <DebugTypographyScene scene={scene} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
