
export type VisualType =
  | "IMAGE"
  | "IMAGE_WITH_TEXT"
  | "IMAGE_GROUP"
  | "TYPOGRAPHY"
  | "NONE";

export type TypographyType =
  | "QUESTION"
  | "KEY_LINE"
  | "DATE"
  | "NORMAL";

export type WordTiming = {
  word: string;
  start: number;
  end: number;
  score?: number;
};

export type RenderScene = {
  scene_id: number;
  script_id?: number;
  script?: string;
  start: number;
  end: number;
  type: VisualType;

  image?: string | null;

  /** Image paths relative to public/. */
  images?: string[];

  /** Key from IMAGE_PRESETS in design/imagePresets.ts. */
  image_preset?: string;

  text?: string | null;
  typography_type?: TypographyType;
  words?: WordTiming[];
};

export type RenderManifest = {
  video: {
    width: number;
    height: number;
    fps: number;
  };
  audio?: {
    path: string;
  };
  scenes: RenderScene[];
};

