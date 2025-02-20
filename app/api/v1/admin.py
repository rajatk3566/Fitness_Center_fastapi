from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...core.config import settings
from ...database import get_db
from ...models.user import User as UserModel
from ...models.member import Member as MemberModel
from ...schema.member import Member, MemberCreate, MemberUpdate
from ..deps import get_current_admin_user

router = APIRouter()

@router.post("/members", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member(
    *,
    db: Session = Depends(get_db),
    member_in: MemberCreate,
    _: UserModel = Depends(get_current_admin_user)
):
    user = db.query(UserModel).filter(UserModel.id == member_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    existing_member = db.query(MemberModel).filter(
        MemberModel.user_id == member_in.user_id
    ).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already exists for this user"
        )

    db_member = MemberModel(**member_in.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@router.put("/members/{member_id}", response_model=Member)
def update_member(
    *,
    db: Session = Depends(get_db),
    member_id: int,
    member_in: MemberUpdate,
    _: UserModel = Depends(get_current_admin_user)
):
   
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    for field, value in member_in.model_dump(exclude_unset=True).items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)
    return member

@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    *,
    db: Session = Depends(get_db),
    member_id: int,
    _: UserModel = Depends(get_current_admin_user)
):
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    db.delete(member)
    db.commit()
    return None

@router.get("/members", response_model=List[Member])
def get_all_members(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: UserModel = Depends(get_current_admin_user)
):
    members = db.query(MemberModel).offset(skip).limit(limit).all()
    return members

@router.get("/memberships", response_model=List[Member])
def get_membership_records(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: UserModel = Depends(get_current_admin_user)
):
    members = (
        db.query(MemberModel)
        .filter(MemberModel.membership_status == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return members