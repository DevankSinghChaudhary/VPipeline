from pydantic import BaseModel


# Output response for the /VPipeline/src/vcp/service/image_search/wikimedia.py
class WikimediaAsset(BaseModel):
    title: str
    url: str
    thumburl: str | None = None
    descriptionurl: str | None = None
    width: int
    height: int
    mime: str
    description: str = ""
    license: str = ""
    artist: str = ""
    credit: str = ""
    usage_terms: str = ""
    license_url: str = ""
