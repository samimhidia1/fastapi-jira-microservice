from pydantic import BaseModel, field_validator
from typing import Optional, Dict
import json

class IssueBase(BaseModel):
    summary: str
    description: str
    project_key: str
    custom_fields: Optional[Dict] = {}

    @field_validator('custom_fields', mode='before')
    def deserialize_custom_fields(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

class IssueCreate(IssueBase):
    issuetype: str
    epic_id: Optional[str] = None
    parent_id: Optional[str] = None

class Epic(IssueBase):
    id: str

class Story(IssueBase):
    id: str
    epic_id: str

class Task(IssueBase):
    id: str
    story_id: str

class TestCase(IssueBase):
    id: str
    task_id: str
