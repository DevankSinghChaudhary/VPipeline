import {Composition} from "remotion";
import {Video} from "./Video";
import type {VideoData} from "./data/types";

const testData: VideoData = {
  audio: "audio/test.mp3",

  scenes: [
    {
      template: "text",

      duration: 4,

      text: {
        content: "THE UNIVERSE",
        color: "primary",
        texture: "text",
        textureOpacity: 0.18,
      },
    },

    {
      template: "image",

      duration: 5,

      image: {
        src: "images/test.jpg",
        texture: "image",
        textureOpacity: 0.12,
      },
    },

    {
      template: "text",

      duration: 4,

      text: {
        content: "IS EXPANDING",
        color: "accent",
        texture: "text",
        textureOpacity: 0.18,
      },
    },
  ],
};

export const RemotionRoot = () => {
  const duration = testData.scenes.reduce(
    (total, scene) => total + scene.duration,
    0,
  );

  return (
    <Composition
      id="VPipeline"
      component={Video}
      durationInFrames={Math.ceil(duration * 30)}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        data: testData,
      }}
    />
  );
};
