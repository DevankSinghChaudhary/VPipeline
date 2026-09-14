import React, {useMemo} from "react";
import {COLORS} from "../design/colors";

/*
 * Static fine-grain approximation of Figma Mono noise.
 *
 * Important:
 * - generated once, not once per frame
 * - no radial gradients
 * - no useCurrentFrame
 * - very low effective opacity
 *
 * The canvas is converted to a data URL once and then reused by
 * the browser for every frame.
 */

const WIDTH = 256;
const HEIGHT = 256;
const DENSITY = 0.50;

export const ProceduralNoise: React.FC = () => {
  const dataUrl = useMemo(() => {
    if (typeof document === "undefined") {
      return undefined;
    }

    const canvas = document.createElement("canvas");
    canvas.width = WIDTH;
    canvas.height = HEIGHT;

    const context = canvas.getContext("2d");

    if (!context) {
      return undefined;
    }

    const image = context.createImageData(WIDTH, HEIGHT);
    const data = image.data;

    let seed = 0x12345678;

    const random = () => {
      seed |= 0;
      seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };

    for (let i = 0; i < WIDTH * HEIGHT; i++) {
      const pixel = i * 4;

      if (random() < DENSITY) {
        data[pixel] = 0;
        data[pixel + 1] = 0;
        data[pixel + 2] = 0;
        data[pixel + 3] = Math.round(COLORS.noise.opacity * 255);
      } else {
        data[pixel] = 0;
        data[pixel + 1] = 0;
        data[pixel + 2] = 0;
        data[pixel + 3] = 0;
      }
    }

    context.putImageData(image, 0, 0);

    return canvas.toDataURL("image/png");
  }, []);

  if (!dataUrl) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        backgroundImage: `url(${dataUrl})`,
        backgroundRepeat: "repeat",
        backgroundSize: "256px 256px",
        opacity: 0.22,
        mixBlendMode: "multiply",
      }}
    />
  );
};
