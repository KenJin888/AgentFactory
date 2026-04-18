from pydantic import BaseModel
from typing import Optional


class CreateSkillRequest(BaseModel):
    name: str
    url: Optional[str] = None


class UpdateSkillRequest(BaseModel):
    content: str