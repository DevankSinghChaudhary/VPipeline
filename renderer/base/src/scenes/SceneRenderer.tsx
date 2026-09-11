import type {SceneData} from "../data/types";
import {TextScene} from "../templates/TextScene";
import {ImageScene} from "../templates/ImageScene";

export const SceneRenderer = ({
  scene,
}: {
  scene: SceneData;
}) => {
  switch (scene.template) {
    case "text":
      return <TextScene scene={scene} />;

    case "image":
      return <ImageScene scene={scene} />;

    default:
      throw new Error(
        `Unknown template: ${scene.template}`,
      );
  }
};
