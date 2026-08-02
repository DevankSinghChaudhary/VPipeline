import geopandas as gpd
from pathlib import Path
from vcp.utils import root

DATASET = root.find() / "src" / "vcp" / "globe" / "packages" / "natural_earth_vector.gpkg"
EXTRACTED = root.find() / "src" / "vcp" / "globe" / "extracted"

layers = gpd.list_layers(DATASET)

for layer in layers["name"]:
    geo = gpd.read_file(
        DATASET,
        layer=layer,
    )

    if "_10m_" in layer:
        out = EXTRACTED / "10m"
    elif "_50m_" in layer:
        out = EXTRACTED / "50m"
    else:
        out = EXTRACTED / "110m"

    out.mkdir(parents=True, exist_ok=True)

    geo.to_file(
        out / f"{layer}.geojson",
        driver="GeoJSON",
    )
