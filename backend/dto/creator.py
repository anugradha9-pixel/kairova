from pydantic import BaseModel, ConfigDict


class CreatorDTO(BaseModel):
    id: int
    name: str
    niche: str
    followers: int

    model_config = ConfigDict(from_attributes=True)


class CreateCreatorResponse(BaseModel):
    creator: CreatorDTO