import {Img, staticFile} from "remotion";
import {textures} from "../design/textures";
import type {TextureName} from "../data/types";

type Props = {
  src: string;

  texture?: TextureName;

  textureOpacity?: number;
};

export const TexturedImage = ({
  src,
  texture = "image",
  textureOpacity = 0.12,
}: Props) => {
  return (
    <div className="relative h-full w-full overflow-hidden">
      <Img
        src={staticFile(src)}
        className="h-full w-full object-cover"
      />

      {texture && (
        <Img
          src={staticFile(textures[texture])}
          className="pointer-events-none absolute inset-0 h-full w-full object-cover"
          style={{
            opacity: textureOpacity,
            mixBlendMode: "overlay",
          }}
        />
      )}
    </div>
  );
};
