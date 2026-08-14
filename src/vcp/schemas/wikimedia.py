from pydantic import BaseModel


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
