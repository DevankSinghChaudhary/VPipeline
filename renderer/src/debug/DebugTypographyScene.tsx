import React from "react";
import {
  AbsoluteFill,
  Audio,
  useCurrentFrame,
  useVideoConfig,
  staticFile
} from "remotion";
import type { ManifestScene } from "../base/data/types";

type Props = {
  scene: ManifestScene;
};

const BACKGROUND = "#FBFAEA";
const TEXT = "#202020";

export const DebugTypographyScene: React.FC<Props> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const time = frame / fps;

  const activeWord = scene.audio.words.find(
    (word) => time >= word.start && time < word.end,
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: BACKGROUND,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Audio src={staticFile(scene.audio.path)} volume={0.6} />

      {activeWord && (
        <div
          style={{
            color: TEXT,
            fontFamily: "Encode Sans Semi Condensed, sans-serif",
            fontSize: 110,
            fontWeight: 700,
            lineHeight: 1,
            textAlign: "center",
          }}
        >
          {activeWord.word}
        </div>
      )}
    </AbsoluteFill>
  );
};
