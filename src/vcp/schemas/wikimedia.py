from pydantic import BaseModel

#Output response for the /VPipeline/src/vcp/service/image_search/wikimedia.py
class WikimediaAsset(BaseModel):
    title: str
    url: str
    thumbnail_url: str | None = None
    page_url: str
    description: str | None = None
    artist: str | None = None
    license: str | None = None
    license_url: str | None = None
    mime: str
    width: int | None = None
    height: int | None = None
