import React from "react";
import { staticFile } from "remotion";
import { LowerThird } from "../../../renderer-collection/typography/lower-third";

export const LowerThirdPreview: React.FC = () => {
  return (
    <LowerThird
      main="Enrico Fermi"
      subtitle="Physicist"
      image={staticFile(
        "images/Informal_Portrait_of_Enrico_Fermi.jpg",
      )}
    />
  );
};
