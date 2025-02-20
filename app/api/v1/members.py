from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from ...database import get_db
from ...models.user import User as UserModel
from ...models.member import Member as MemberModel
from ...schema.member import Member, MemberUpdate
from ..deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=Member)
def get_membership_status(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    member = db.query(MemberModel).filter(
        MemberModel.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    return member

@router.post("/renew")
def renew_membership(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    member = db.query(MemberModel).filter(
        MemberModel.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    
    new_start = max(member.membership_end, datetime.now())
    member.membership_end = new_start + timedelta(days=30)
    member.membership_status = True
    
    db.commit()
    db.refresh(member)
    
    return {
        "message": "Membership renewed successfully",
        "new_end_date": member.membership_end
    }

@router.get("/history", response_model=List[dict])
def get_membership_history(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    member = db.query(MemberModel).filter(
        MemberModel.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    history = [
        {
            "event_type": "membership_start",
            "date": member.membership_start,
            "details": "Initial membership start"
        },
        {
            "event_type": "membership_end",
            "date": member.membership_end,
            "details": "Current membership end date"
        }
    ]
    
    return history