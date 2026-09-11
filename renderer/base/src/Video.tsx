import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
} from "remotion";

import type {VideoData} from "./data/types";
import {Background} from "./components/Background";
import {SceneRenderer} from "./scenes/SceneRenderer";

export const Video = ({
  data,
}: {
  data: VideoData;
}) => {
  let currentFrame = 0;

  return (
    <AbsoluteFill>
      {/* Global background */}
      <Background />

      {/* Scenes */}
      <AbsoluteFill
        style={{
          zIndex: 1,
        }}
      >
        {data.scenes.map((scene, index) => {
          const startFrame = currentFrame;

          const durationInFrames = Math.round(
            scene.duration * 30,
          );

          currentFrame += durationInFrames;

          return (
            <Sequence
              key={index}
              from={startFrame}
              durationInFrames={durationInFrames}
            >
              <SceneRenderer scene={scene} />
            </Sequence>
          );
        })}
      </AbsoluteFill>

      {/* Audio */}
      <Audio src={staticFile(data.audio)} />
    </AbsoluteFill>
  );
};
