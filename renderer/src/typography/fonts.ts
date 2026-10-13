import { loadFont as loadEncodeSans } from "@remotion/google-fonts/EncodeSansSemiCondensed";
import { loadFont as loadEphesis } from "@remotion/google-fonts/Ephesis";

const encodeSans = loadEncodeSans("normal", {
  weights: ["700"],
  subsets: ["latin"],
});

const ephesis = loadEphesis("normal", {
  weights: ["400"],
  subsets: ["latin"],
});

export const TYPOGRAPHY_FONTS = {
  bold: encodeSans.fontFamily,
  calligraphic: ephesis.fontFamily,
};

export const waitForTypographyFonts = async () => {
  await Promise.all([
    encodeSans.waitUntilDone(),
    ephesis.waitUntilDone(),
  ]);
};
