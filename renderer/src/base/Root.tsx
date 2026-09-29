import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { rendererManifest } from "./data/manifest";
import { FPS, getTotalDurationInFrames } from "./utils/timeline";

import { LowerThirdPreview } from "./preview/LowerThird";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="LowerThirdPreview"
        component={LowerThirdPreview}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
