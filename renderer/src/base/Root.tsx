import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { rendererManifest } from "./data/manifest";
import { FPS, getTotalDurationInFrames } from "./utils/timeline";

export const RemotionRoot: React.FC = () => {
  const durationInFrames = getTotalDurationInFrames(rendererManifest);

  return (
    <Composition
      id="VPipeline"
      component={Video}
      durationInFrames={durationInFrames}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
