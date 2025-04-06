from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.group import GroupCreate, GroupOut
from app.api.deps import get_db, get_current_user
from app.crud.crud_group import create_group, get_groups
from app.db.models.user import User
from fastapi import Path
from app.crud.crud_group import add_user_to_group,get_group_members
from app.services.split_service import calculate_balances
from app.schemas.user import UserOut

router = APIRouter()

@router.post("/", response_model=GroupOut)
def create_new_group(
    group_in: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_group(db, group_in)

@router.get("/", response_model=list[GroupOut])
def list_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_groups(db)



@router.get("/{group_id}/balances")
def get_balances(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    balances = calculate_balances(db, group_id)
    return balances


@router.post("/{group_id}/join", response_model=GroupOut)
def join_group(
    group_id: int = Path(..., description="The ID of the group to join"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = add_user_to_group(db, group_id, current_user)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.get("/my-groups")
def get_my_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return current_user.groups


@router.get("/{group_id}/users", response_model=List[UserOut])
def get_group_users(group_id: int, db: Session = Depends(get_db)):
    users = get_group_members(db, group_id)
    if users is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return users

