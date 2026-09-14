export type TypographyType = "KEY_LINE" | "QUESTION" | "DATE" | "NORMAL";

export type WordTiming = {
  word: string;
  start: number;
  end: number;
  score?: number;
};

export type SceneData = {
  scene_id: number;
  type: "TYPOGRAPHY";
  audio: {
    path: string;
    duration: number;
    result: WordTiming[];
  };
  typography: {
    type: TypographyType;
    text: string;
  };
};
