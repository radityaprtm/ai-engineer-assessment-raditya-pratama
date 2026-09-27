from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=500
    )


class Source(BaseModel):
    type: str
    name: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]