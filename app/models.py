from pydantic import BaseModel, Field, ConfigDict


class AskRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    question: str = Field(
        min_length=2,
        max_length=500,
        strict=True,
    )

    
class Source(BaseModel):
    type: str
    name: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]