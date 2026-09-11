export type ColorName =
  | "background"
  | "primary"
  | "secondary"
  | "accent";

export type TextureName =
  | "grain"
  | "text"
  | "image";

export type TextData = {
  content: string;

  color?: ColorName;
  texture?: TextureName;
  textureOpacity?: number;
};

export type ImageData = {
  src: string;

  texture?: TextureName;
  textureOpacity?: number;
};

export type TextSceneData = {
  template: "text";

  duration: number;

  text: TextData;
};

export type ImageSceneData = {
  template: "image";

  duration: number;

  image: ImageData;
};

export type SceneData =
  | TextSceneData
  | ImageSceneData;

export type VideoData = {
  audio: string;

  scenes: SceneData[];
};
