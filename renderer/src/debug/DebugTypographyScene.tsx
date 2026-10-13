import React from "react";
import {
  AbsoluteFill,
  Audio,
  useCurrentFrame,
  useVideoConfig,
  staticFile
} from "remotion";

import type { ManifestScene } from "../base/data/types";

import {
  TYPOGRAPHY_STYLES,
  createTypographyGroups,
} from "../typography/typography-styles";

type Props = {
  scene: ManifestScene;
};

const BACKGROUND = "#FBFAEA";

export const DebugTypographyScene: React.FC<Props> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const time = frame / fps;
  const words = scene.audio.words;

  // Find the most recently started word.
  // This avoids flickering between WhisperX timestamps.
  const lastStartedIndex = words.reduce(
    (lastIndex, word, index) =>
      time >= word.start ? index : lastIndex,
    -1,
  );

  const groups = createTypographyGroups(
    words.length,
    scene.scene_id,
  );

  const currentGroup = groups.find(
    (group) =>
      lastStartedIndex >= group.start &&
      lastStartedIndex < group.end,
  );

  const visibleWords =
    currentGroup && lastStartedIndex >= 0
      ? words.slice(
          currentGroup.start,
          lastStartedIndex + 1,
        )
      : [];

  const style = currentGroup
    ? TYPOGRAPHY_STYLES[currentGroup.styleIndex]
    : TYPOGRAPHY_STYLES[0];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: BACKGROUND,
        justifyContent: "center",
        alignItems: "center",
        padding: 120,
      }}
    >
      <Audio src={staticFile(scene.audio.path)} />

      <div
        style={{
          fontFamily: style.fontFamily,
          fontSize: 100,
          fontWeight: style.fontWeight,
          color: style.color,
          lineHeight: 1.05,
          textAlign: "center",
          maxWidth: "85%",
        }}
      >
        {visibleWords.map((word, index) => (
          <React.Fragment
            key={`${word.start}-${word.end}-${index}`}
          >
            {index > 0 ? " " : ""}
            {word.word}
          </React.Fragment>
        ))}
      </div>
    </AbsoluteFill>
  );
};
