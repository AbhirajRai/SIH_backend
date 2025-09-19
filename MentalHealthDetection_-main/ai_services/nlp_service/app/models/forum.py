from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class ForumPost(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: Optional[str]
    topic: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    flagged: bool = False
    reports: int = 0  # Number of reports

class ForumReport(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    post_id: str
    reporter_id: Optional[str]
    reason: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
