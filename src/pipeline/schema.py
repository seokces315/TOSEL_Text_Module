from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


# Pydantic class for Data Schema
class Content(BaseModel):
    type: str = "T"
    text: str


class Material(BaseModel):
    index: int
    content: Content


class Ask(BaseModel):
    type: str = "T"
    text: str


class Choice(BaseModel):
    index: int
    content: Content
    isCorrect: bool


class Item(BaseModel):
    materials: List[Material]
    ask: Ask
    choices: List[Choice]
    tags: List[Dict[str, Any]] = Field(default_factory=list)
    difficulty: Optional[int] = None
    predictedAccuracy: Optional[int] = None
    createdUserId: Optional[int] = None
