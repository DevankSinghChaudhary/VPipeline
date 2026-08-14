from pydantic import BaseModel, Field


class AssetResponse(BaseModel):
    can_be_get_as_an_asset: bool = Field(description="The Segments can be classified as assets or not? like image, person's image, map etc. If idea is category then look the idea if related to something that can be get as an asset.")
