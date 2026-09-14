import React from "react";
import {COLORS} from "../design/colors";
import {FONTS} from "../design/fonts";

type Props = {
  text: string;
  color?: string;
  fontSize?: number;
};

export const TexturedText: React.FC<Props> = ({
  text,
  color = COLORS.text.primary,
  fontSize = 92,
}) => (
  <div
    style={{
      fontFamily: FONTS.primary,
      fontWeight: 700,
      fontSize,
      lineHeight: 1.02,
      letterSpacing: "-0.025em",
      color,
      textAlign: "center",
      maxWidth: 1450,
      whiteSpace: "pre-wrap",
    }}
  >
    {text}
  </div>
);
