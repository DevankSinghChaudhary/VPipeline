import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { rendererManifest } from "./data/manifest";
import { SceneRenderer } from "./scenes/SceneRenderer";
import { getSceneDurationInFrames } from "./utils/timeline";

export const Video: React.FC = () => {
  let currentFrame = 0;

  return (
    <AbsoluteFill>
      {rendererManifest.map((scene) => {
        const durationInFrames = getSceneDurationInFrames(scene);
        const from = currentFrame;
        currentFrame += durationInFrames;

        return (
          <Sequence
            key={scene.scene_id}
            from={from}
            durationInFrames={durationInFrames}
          >
            <AbsoluteFill>
              <SceneRenderer scene={scene} />
              <Audio src={staticFile(scene.audio.path)} />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
