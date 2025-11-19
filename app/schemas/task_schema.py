from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[date]
    owner_email: str
    created_at: datetime
