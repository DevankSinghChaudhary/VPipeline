from pydantic import BaseModel, Field

#Structure same as ScriptResponse @ ./script.py 
#but for Formatter @ /VPipeline/src/vcp/nodes/format/format.py
class FormatSingle(BaseModel):
    id: int
    script: str

class FormatResponse(BaseModel):
    script: list[FormatSingle]
