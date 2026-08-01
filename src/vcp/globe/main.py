import geopandas as gpd
from vcp.utils import root

DATASET = root.find() / "src" / "dataset" / "globe" / "packages" / "natural_earth_vector.gpkg"

land = gpd.read_file(
    DATASET,
    layer="ne_110m_land"
)

land.to_file(
    "land.geojson",
    driver="GeoJSON"
)
