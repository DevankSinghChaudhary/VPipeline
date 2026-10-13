
export type ImageEnterAnimation =
  | "fade"
  | "fade-slide-up"
  | "fade-slide-side"
  | "scale-in"
  | "none";

/**
 * Coordinates are fractions of the full composition (0–1), not pixels.
 * Images stay inside these boxes; they never become full-screen backgrounds.
 */
export type ImageSlot = {
  x: number;
  y: number;
  width: number;
  height: number;
  radius: number;
  fit: "cover" | "contain";
  rotation: number;
  zIndex: number;
  floatY?: number;
  floatRotation?: number;
};

export type ImageLayoutPreset = {
  label: string;
  description: string;
  slots: ImageSlot[];
  animation: {
    enter: ImageEnterAnimation;
    durationInFrames: number;
    staggerInFrames: number;
  };
};

const gentleEntrance: ImageLayoutPreset["animation"] = {
  enter: "fade-slide-up",
  durationInFrames: 18,
  staggerInFrames: 5,
};

export const IMAGE_PRESETS = {
  "portrait-right": {
    label: "Portrait Card",
    description: "One tall image on the right, with space for typography on the left.",
    slots: [
      {
        x: 0.69,
        y: 0.17,
        width: 0.23,
        height: 0.66,
        radius: 22,
        fit: "cover",
        rotation: 0,
        zIndex: 1,
      },
    ],
    animation: gentleEntrance,
  },

  "portrait-left": {
    label: "Portrait Left",
    description: "One tall image on the left, with space for typography on the right.",
    slots: [
      {
        x: 0.08,
        y: 0.17,
        width: 0.23,
        height: 0.66,
        radius: 22,
        fit: "cover",
        rotation: 0,
        zIndex: 1,
      },
    ],
    animation: gentleEntrance,
  },

  "landscape-right": {
    label: "Landscape Card",
    description: "One wide image on the right.",
    slots: [
      {
        x: 0.64,
        y: 0.28,
        width: 0.29,
        height: 0.42,
        radius: 18,
        fit: "cover",
        rotation: 0,
        zIndex: 1,
      },
    ],
    animation: gentleEntrance,
  },

  "double-stack": {
    label: "Double Stack",
    description: "Two overlapping image cards with gentle floating motion.",
    slots: [
      {
        x: 0.65,
        y: 0.22,
        width: 0.24,
        height: 0.51,
        radius: 18,
        fit: "cover",
        rotation: 5,
        zIndex: 1,
        floatY: 3,
        floatRotation: 0.8,
      },
      {
        x: 0.72,
        y: 0.29,
        width: 0.22,
        height: 0.49,
        radius: 18,
        fit: "cover",
        rotation: -4,
        zIndex: 2,
        floatY: 4,
        floatRotation: -0.8,
      },
    ],
    animation: {
      enter: "scale-in",
      durationInFrames: 20,
      staggerInFrames: 6,
    },
  },

  "triple-stack": {
    label: "Triple Stack",
    description: "Three overlapping cards with varied angles and depth order.",
    slots: [
      {
        x: 0.63,
        y: 0.20,
        width: 0.22,
        height: 0.47,
        radius: 14,
        fit: "cover",
        rotation: -7,
        zIndex: 1,
        floatY: 2,
        floatRotation: 0.6,
      },
      {
        x: 0.70,
        y: 0.26,
        width: 0.22,
        height: 0.47,
        radius: 14,
        fit: "cover",
        rotation: 5,
        zIndex: 2,
        floatY: 3,
        floatRotation: -0.6,
      },
      {
        x: 0.76,
        y: 0.32,
        width: 0.19,
        height: 0.43,
        radius: 14,
        fit: "cover",
        rotation: -2,
        zIndex: 3,
        floatY: 4,
        floatRotation: 0.5,
      },
    ],
    animation: {
      enter: "fade-slide-side",
      durationInFrames: 22,
      staggerInFrames: 5,
    },
  },

  "filmstrip-bottom": {
    label: "Filmstrip",
    description: "Three landscape images aligned along the bottom.",
    slots: [
      {
        x: 0.10,
        y: 0.65,
        width: 0.23,
        height: 0.20,
        radius: 8,
        fit: "cover",
        rotation: 0,
        zIndex: 1,
      },
      {
        x: 0.385,
        y: 0.65,
        width: 0.23,
        height: 0.20,
        radius: 8,
        fit: "cover",
        rotation: 0,
        zIndex: 1,
      },
      {
        x: 0.67,
        y: 0.65,
        width: 0.23,
        height: 0.20,
        radius: 8,
        fit: "cover",
        rotation: 0,
        zIndex: 1,
      },
    ],
    animation: {
      enter: "fade",
      durationInFrames: 16,
      staggerInFrames: 4,
    },
  },

  "floating-collage": {
    label: "Floating Collage",
    description: "A compact collage with subtle independent movement.",
    slots: [
      {
        x: 0.68,
        y: 0.15,
        width: 0.19,
        height: 0.30,
        radius: 16,
        fit: "cover",
        rotation: -7,
        zIndex: 2,
        floatY: 4,
        floatRotation: 0.8,
      },
      {
        x: 0.78,
        y: 0.43,
        width: 0.16,
        height: 0.25,
        radius: 12,
        fit: "cover",
        rotation: 6,
        zIndex: 3,
        floatY: 3,
        floatRotation: -0.7,
      },
      {
        x: 0.62,
        y: 0.55,
        width: 0.17,
        height: 0.23,
        radius: 12,
        fit: "cover",
        rotation: -3,
        zIndex: 1,
        floatY: 3,
        floatRotation: 0.5,
      },
    ],
    animation: {
      enter: "fade-slide-up",
      durationInFrames: 20,
      staggerInFrames: 4,
    },
  },
} satisfies Record<string, ImageLayoutPreset>;

export type ImagePresetName = keyof typeof IMAGE_PRESETS;

