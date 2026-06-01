from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be blank or whitespace only")
        return value.strip()


class UserResponse(BaseModel):
    id: str
    name: str
    api_key: str


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_project_name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Project name cannot be blank or whitespace only")
        return value.strip()



class ProjectResponse(BaseModel):
    id: str
    name: str
    owner_id: str
    created_at: datetime
    updated_at: datetime



class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_task_title_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Task title cannot be blank or whitespace only")
        return value.strip()



class TaskResponse(BaseModel):
    id: str
    title: str
    status: str
    project_id: str
    created_at: datetime
    updated_at: datetime



class TaskUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]