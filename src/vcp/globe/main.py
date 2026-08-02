import geopandas as gpd
from vcp.utils import root

DATASET = root.find() / "src" / "vcp" / "globe" / "packages" / "natural_earth_vector.gpkg"
EXTRACTED = root.find() / "src" / "vcp" / "globe" / "extracted"

layers = gpd.list_layers(DATASET)
for layer in layers["name"]:
    print(layer)

input = input("Enter File to Extract: ")

land = gpd.read_file(
    DATASET,
    layer=input
)

land.to_file(
        f"{EXTRACTED}/{input}.geojson",
        driver="GeoJSON"
)
