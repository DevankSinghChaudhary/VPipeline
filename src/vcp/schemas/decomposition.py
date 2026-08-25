from typing import Literal

from pydantic import BaseModel, Field

Modality = Literal["image", "typography"]


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
    visual_modalities: list[Modality] = Field(
        description=f"Modality of the scene required from {Modality}"
    )
    primary_modality: Modality = Field(
        description=f"Primary modality of the scene, modality means what this scene wants from {Modality}, like what fits scene better, which type either typography or image convey the script better."
    )
    secondary_modality: Modality | None = Field(
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
