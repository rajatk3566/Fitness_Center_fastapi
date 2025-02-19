from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemberBase(BaseModel):
    membership_status: bool
    membership_start: datetime
    membership_end: datetime

class MemberCreate(MemberBase):
    user_id: int

class MemberUpdate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True