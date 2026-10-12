import { Composition } from "remotion";
import manifest from "../data/RendererManifest.json";

import { Video } from "./Video";

const FPS = 30;

const totalDuration = manifest.reduce(
  (total, scene) => total + scene.duration,
  0
);

export const RemotionRoot = () => {
  return (
    <Composition
      id="VPipeline"
      component={Video}
      durationInFrames={Math.ceil(totalDuration * FPS)}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{
        manifest,
      }}
    />
  );
};
