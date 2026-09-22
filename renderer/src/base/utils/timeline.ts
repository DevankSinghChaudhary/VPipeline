import type { ManifestScene } from "../data/types";

export const FPS = 30;

export function getSceneDurationInFrames(
  scene: ManifestScene,
): number {
  return Math.ceil(scene.duration * FPS);
}

export function getTotalDurationInFrames(
  scenes: ManifestScene[],
): number {
  return scenes.reduce(
    (total, scene) => total + getSceneDurationInFrames(scene),
    0,
  );
}
