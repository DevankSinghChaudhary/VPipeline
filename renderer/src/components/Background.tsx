import {AbsoluteFill, staticFile} from "remotion";
import {colors} from "../design/colors";
import {textures} from "../design/textures";

type Props = {
  texture?: keyof typeof textures;
  textureOpacity?: number;
  textureSize?: string;
  textureBlendMode?: React.CSSProperties["mixBlendMode"];
  textureContrast?: number;
  textureBrightness?: number;
  textureBlur?: number;
  textureShadow?: string;
};

export const Background = ({
  texture = "paper",
  textureOpacity = 0.8,
  textureSize = "fill",
  textureBlendMode = "multiply",
  textureContrast = 1,
  textureBrightness = 0.75,
  textureBlur = 0.1,
  textureShadow = "0 1px 3px rgba(0, 0, 0, 0.12",
}: Props) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.background,
        overflow: "hidden",
        zIndex: 0,
      }}
    >
      {/* Texture */}
      <div
        style={{
          position: "absolute",
          inset: 0,

          backgroundImage: `url(${staticFile(
            textures[texture],
          )})`,

          backgroundSize: textureSize,
          backgroundPosition: "center",
          backgroundRepeat: "repeat",

          opacity: textureOpacity,

          mixBlendMode: textureBlendMode,

          filter: `
            contrast(${textureContrast})
            brightness(${textureBrightness})
            blur(${textureBlur}px)
            ${textureShadow !== "none"
              ? `drop-shadow(${textureShadow})`
              : ""}
          `,

          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
