from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.expense import ExpenseCreate, ExpenseOut
from app.api.deps import get_db, get_current_user
from app.crud.crud_expense import create_expense, get_expenses_for_group
from app.db.models.user import User
from typing import Optional, Dict
from enum import Enum

router = APIRouter()

@router.post("/", response_model=ExpenseOut)
def add_expense(
    expense_in: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a new expense to a group.

    - Equal: Just pass amount, group_id, split_type = equal
    - Unequal: Add split_details = {user_id: amount}
    - Percentage: split_details = {user_id: percent}
    """    
    return create_expense(db, expense_in, current_user)

@router.get("/{group_id}", response_model=list[ExpenseOut])
def list_expenses(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_expenses_for_group(db, group_id)
