
import React from "react";
import {
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

import { Background } from "../components/Background";
import {
  IMAGE_PRESETS,
  type ImageEnterAnimation,
} from "../design/imagePresets";
import type { RenderScene } from "../data/types";

const entranceStyle = (
  animation: ImageEnterAnimation,
  progress: number,
) => {
  const opacity = animation === "none" ? 1 : progress;

  const rise =
    animation === "fade-slide-up"
      ? (1 - progress) * 24
      : 0;

  const side =
    animation === "fade-slide-side"
      ? (1 - progress) * 28
      : 0;

  const scale =
    animation === "scale-in"
      ? 0.92 + progress * 0.08
      : 1;

  return {
    opacity,
    translateX: side,
    translateY: rise,
    scale,
  };
};

export const ImageGroupScene: React.FC<{
  scene: RenderScene;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const presetName = scene.image_preset ?? "portrait-right";

  const preset =
    IMAGE_PRESETS[
      presetName as keyof typeof IMAGE_PRESETS
    ] ?? IMAGE_PRESETS["portrait-right"];

  const images =
    scene.images ?? (scene.image ? [scene.image] : []);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        overflow: "hidden",
      }}
    >
      <Background />

      {preset.slots.map((slot, index) => {
        const image = images[index];

        if (!image) return null;

        const delay =
          index * preset.animation.staggerInFrames;

        const duration = Math.max(
          1,
          preset.animation.durationInFrames,
        );

        const progress = interpolate(
          frame - delay,
          [0, duration],
          [0, 1],
          {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          },
        );

        const entrance = entranceStyle(
          preset.animation.enter,
          progress,
        );

        const phase =
          ((frame / fps) + index * 0.8) *
          (Math.PI * 2 / 4.5);

        const floatY =
          (slot.floatY ?? 0) * Math.sin(phase);

        const floatRotation =
          (slot.floatRotation ?? 0) * Math.sin(phase);

        return (
          <div
            key={`${scene.scene_id}-${index}`}
            style={{
              position: "absolute",

              left: `${slot.x * 100}%`,
              top: `${slot.y * 100}%`,
              width: `${slot.width * 100}%`,
              height: `${slot.height * 100}%`,

              zIndex: slot.zIndex,

              borderRadius: slot.radius,
              overflow: "hidden",

              backgroundColor: "rgba(32, 32, 32, 0.06)",

              boxShadow:
                slot.rotation === 0
                  ? "0 8px 28px rgba(32, 32, 32, 0.10)"
                  : "0 12px 30px rgba(32, 32, 32, 0.14)",

              opacity: entrance.opacity,

              transform: [
                `translate(${entrance.translateX}px, ${
                  entrance.translateY + floatY
                }px)`,
                `scale(${entrance.scale})`,
                `rotate(${slot.rotation + floatRotation}deg)`,
              ].join(" "),

              transformOrigin: "center center",
            }}
          >
            <Img
              src={staticFile(image)}
              style={{
                display: "block",
                width: "100%",
                height: "100%",
                objectFit: slot.fit,
              }}
            />
          </div>
        );
      })}
    </div>
  );
};

