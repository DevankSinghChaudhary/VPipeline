import {AbsoluteFill} from "remotion";
import type {TextSceneData} from "../data/types";
import {TexturedText} from "../components/TexturedText";

export const TextScene = ({
  scene,
}: {
  scene: TextSceneData;
}) => {
  return (
    <AbsoluteFill
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "120px",
      }}
    >
      <TexturedText
        text={scene.text.content}
        color={scene.text.color}
        texture={scene.text.texture}
        textureOpacity={scene.text.textureOpacity}
      />
    </AbsoluteFill>
  );
};
