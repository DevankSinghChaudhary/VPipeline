import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import type { ManifestScene } from "../base/data/types";

interface Props {
  scene: ManifestScene;
}

export const NoneScene: React.FC<Props> = ({ scene }) => {
  const frame = useCurrentFrame();
  const time = frame / 30;

  const visibleWords = scene.audio.words.filter(
    (word) => word.start <= time,
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#080808",
        alignItems: "center",
        justifyContent: "center",
        padding: 100,
      }}
    >
      <div
        style={{
          color: "white",
          fontSize: 72,
          fontWeight: 700,
          textAlign: "center",
          lineHeight: 1.2,
        }}
      >
        {visibleWords.map((word, index) => (
          <span key={index}>{word.word} </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};
