import {AbsoluteFill} from "remotion";
import {useEffect, useRef} from "react";
import { Map } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import data from './terracotta.json';


export const Globe = () => {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    const map = new Map({
        container: mapRef.current,
        style: data,
        center: [0, 20],
        zoom: 1.8,
        interactive: false,
        attributionControl: false,
        fadeDuration: 0,
    });

}, []);

  return (
    <AbsoluteFill>
      <div
        ref={mapRef}
        style={{
          position: "absolute",
          inset: 0,
        }}
      />
    </AbsoluteFill>
  );
};
