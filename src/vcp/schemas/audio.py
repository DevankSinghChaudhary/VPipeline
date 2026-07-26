from pydantic import BaseModel


class AudioSegment(BaseModel):
    path: str
