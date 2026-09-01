from typing import Literal

from pydantic import BaseModel, Field

MODALITY = Literal["IMAGE", "IMAGE_WITH_TEXT", "TYPOGRAPHY", "NONE"]

IMAGE_MODALITY = Literal["IMAGE", "IMAGE_WITH_TEXT"]
TYPE_TEXT = Literal["QUESTION", "KEY_LINE"]

TYPE_TYPOGRAPHY = Literal["QUESTION", "KEY_LINE", "DATE", "NORMAL"]


class typography(BaseModel):
    required: bool = Field(description="If typography is required, TRUE")
    purpose: str | None = Field(
        default=None,
        description="Purpose of the typography, like why are we adding it.",
    )
    subject: str | None = Field(
        default=None,
        description="Subject of typography, what are we focusing on from the script with typography",
    )


class image(BaseModel):
    required: bool = Field(description="If Image is required, TRUE")
    purpose: str | None = Field(
        default=None, description="Purpose of the image, like why wre we adding it."
    )
    subject: str | None = Field(
        default=None,
        description="Subject og image, what are we focusing on from the script with image.",
    )


class decompostioned(BaseModel):
    scene_id: int = Field(description="Scene ID of each script passed")
    visual_modalities: list[MODALITY] = Field(
        description=f"MODALITY of the scene required from {MODALITY}"
    )
    primary_modality: MODALITY = Field(
        description=f"Primary modality of the scene, modality means what this scene wants from {MODALITY}, like what fits scene better, which type either typography or image convey the script better."
    )
    secondary_modality: MODALITY | None = Field(
        default=None,
        description="Secondary modality is because, a scene could need both image and typography, so setting which should be emphasized will go in primary and second in secondary, only if scene need both.",
    )
    reasoning: str = Field(
        description="Basically WHY?, why LLM chose which modality and why?"
    )
    typography: typography
    image: image


class DecompostionResponse(BaseModel):
    scenes: list[decompostioned]


#    NEW TYPE OF RESPONSE IN REPLACEMENT OF DecompostionResponse (IN TESTING)
# ==========================================================================#


class ImageVisual(BaseModel):
    type: IMAGE_MODALITY
    type_text: TYPE_TEXT | None = Field(
        default=None, description="Could be None as type: 'Could be only text'."
    )
    asset: list[str]


class TypographyVisual(BaseModel):
    text: str
    type_typography: TYPE_TYPOGRAPHY


class SingleScene(BaseModel):
    scene_id: int
    script_id: int
    script: str
    segment: list[str]

    visual_modalities: list[MODALITY]

    image: ImageVisual | None
    typography: TypographyVisual | None


class Scene(BaseModel):
    scene: list[SingleScene]
