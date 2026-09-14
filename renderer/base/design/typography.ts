import {COLORS} from "./colors";
import {FONTS} from "./fonts";

export const TYPOGRAPHY = {
  KEY_LINE: {
    fontFamily: FONTS.primary,
    fontWeight: 150,
    color: COLORS.text.primary,
  },
  QUESTION: {
    fontFamily: FONTS.primary,
    fontWeight: 150,
    color: COLORS.text.primary,
  },
  DATE: {
    fontFamily: FONTS.primary,
    fontWeight: 150,
    color: COLORS.text.accent,
  },
  NORMAL: {
    fontFamily: FONTS.primary,
    fontWeight: 150,
    color: COLORS.text.primary,
  },
} as const;
