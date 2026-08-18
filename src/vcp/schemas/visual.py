from pydantic import BaseModel, Field

#Identifier response from LLM (Visualizer) so each segment can be classified as either TRUE or FALSE for direct assets or indirect
#Direct: Like image of any person, map, etc
#Indirect: Like TimeLine of a event then cannot be gathered as asset but can be created seperately.
#How: Basically rought process of how to achieve indirect one but can work for direct as search query on web.
class asset(BaseModel):
    can_be_get_as_an_direct_asset: bool = Field(description="The Segments can be classified as assets or not? like image, person's image, map etc. If idea is category then look the idea if related to something that can be classified as asset, the true if no false")
    can_be_get_as_an_indirect_asset: bool = Field(description="The Segment if can_be_get_as_an_direct_asset=False, LLM will check if it can be get as an indirect asset like 'segment(segment='Over 70 years ago', category='Time Period', can_be_get_as_an_asset=False). In This case it could be get as an asset in form of Time Period like time dial moving from 0 to 70 years or clock. Check like this'")
    how: str = Field(description="Tell how it could be done/gathered as asset, if not even this then make it as well False")

#Single segment of the script that will contain the segment, category of segment like name, timeline, etc and classification=asset^ (defined above)
class segment(BaseModel):
    segment: str = Field(description="Segment from the script")
    category: str = Field(description="Category of the segmented word/scentence. E.g: Person, Building, Date, Place, City, Capital, Country etc")
    classification: asset = Field(description="The Segment if can_be_get_as_an_direct_asset=False, LLM will check if it can be get as an indirect asset like 'segment(segment='Over 70 years ago', category='Time Period', can_be_get_as_an_asset=False). In This case it could be get as an asset in form of Time Period like time dial moving from 0 to 70 years or clock. Check like this'")

#State containing id of script, script and segments.
class visual(BaseModel):
    id: int = Field(description="Integer UID for each script. Starting from 1")
    script: str = Field(description="The original script that being passed to LLM")
    segments: list[segment] = Field(description="Segments from script that LLM passes")

#Final state containing as list of dictionaries:
#VisualResponse(Visual=[
#                   {
#                   id=1,
#                   script="content",
#                   segments=segment(
#                   {
#                   segment="content",category="category of topic",classification=asset(can_be_get_as_an_direct_asset=bool,can_be_get_as_an_indirect_asset=bool,how="explaination")
#               }
#           )
#       }
#   ]
#)
class VisualResponse(BaseModel):
    visual: list[visual]
