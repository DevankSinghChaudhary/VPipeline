import {AbsoluteFill} from "remotion";
import type {ImageSceneData} from "../data/types";
import {TexturedImage} from "../components/TexturedImage";

export const ImageScene = ({
  scene,
}: {
  scene: ImageSceneData;
}) => {
  return (
    <AbsoluteFill className="p-20">
      <TexturedImage
        src={scene.image.src}
        texture={scene.image.texture}
        textureOpacity={scene.image.textureOpacity}
      />
    </AbsoluteFill>
  );
};
