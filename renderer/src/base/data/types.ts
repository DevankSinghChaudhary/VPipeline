export type SceneType =
  | "IMAGE"
  | "IMAGE_WITH_TEXT"
  | "TYPOGRAPHY"
  | "NONE";

export interface WordSegment {
  word: string;
  start: number;
  end: number;
  score?: number;
}

export interface SceneAudio {
  path: string;
  words: WordSegment[];
}

export interface SceneVisual {
  template?: string;
  text?: string;
  image?: string[];
  [key: string]: unknown;
}

export interface ManifestScene {
  scene_id: number;
  type: SceneType;
  duration: number;
  audio: SceneAudio;
  visual: SceneVisual;
}

export type RendererManifest = ManifestScene[];
