import React from "react";
import {Composition} from "remotion";
import {Video} from "./Video";
import {scene} from "./data/scene";

export const Root: React.FC = () => {
  const fps = 30;
  const durationInFrames = Math.max(1, Math.ceil(scene.audio.duration * fps));

  return (
    <Composition
      id="VPipelineBaseTypography"
      component={Video}
      durationInFrames={durationInFrames}
      fps={fps}
      width={1920}
      height={1080}
      defaultProps={{scene}}
    />
  );
};
