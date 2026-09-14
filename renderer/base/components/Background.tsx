import React from "react";
import {COLORS} from "../design/colors";
import {ProceduralNoise} from "./ProceduralNoise";

export const Background: React.FC = () => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      backgroundColor: COLORS.background,
      overflow: "hidden",
    }}
  >
    <ProceduralNoise />
  </div>
);
