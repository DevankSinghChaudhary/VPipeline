import { TYPOGRAPHY_FONTS } from "./fonts";

export const TYPOGRAPHY_STYLES = [
  {
    fontFamily: TYPOGRAPHY_FONTS.bold,
    fontWeight: 700,
    color: "#AE2225",
  },
  {
    fontFamily: TYPOGRAPHY_FONTS.calligraphic,
    fontWeight: 400,
    color: "#202020",
  },
  {
    fontFamily: TYPOGRAPHY_FONTS.bold,
    fontWeight: 700,
    color: "#202020",
  },
  {
    fontFamily: TYPOGRAPHY_FONTS.calligraphic,
    fontWeight: 400,
    color: "#AE2225",
  },
] as const;

export type TypographyStyleIndex =
  keyof typeof TYPOGRAPHY_STYLES extends never
    ? never
    : number;

export type TypographyGroup = {
  start: number;
  end: number;
  styleIndex: number;
};

// Deterministic pseudo-random value in the range [0, 1).
function seededRandom(
  sceneId: number,
  groupIndex: number,
): number {
  let value =
    Math.imul(sceneId + 1, 0x45d9f3b) ^
    Math.imul(groupIndex + 1, 0x27d4eb2d);

  value = Math.imul(value ^ (value >>> 16), 0x45d9f3b);
  value ^= value >>> 16;

  return (value >>> 0) / 4294967296;
}

export function createTypographyGroups(
  wordCount: number,
  sceneId: number,
): TypographyGroup[] {
  const groups: TypographyGroup[] = [];

  let start = 0;
  let previousStyle = -1;

  while (start < wordCount) {
    const groupIndex = groups.length;

    // Each group contains 2 or 3 words.
    const groupSize =
      2 + Math.floor(seededRandom(sceneId, groupIndex) * 2);

    const candidate = Math.floor(
      seededRandom(sceneId + 17, groupIndex) *
        TYPOGRAPHY_STYLES.length,
    );

    // Avoid repeating the previous style combination.
    const styleIndex =
      candidate === previousStyle
        ? (candidate + 1) % TYPOGRAPHY_STYLES.length
        : candidate;

    const end = Math.min(start + groupSize, wordCount);

    groups.push({
      start,
      end,
      styleIndex,
    });

    previousStyle = styleIndex;
    start = end;
  }

  return groups;
}
