import { Composition } from "remotion";
import { Globe } from "./Composition";

export const Root = () => {
  return (
    <Composition
      id="Map"
      component={Globe}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
