from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db.models.user import User
from app.services.split_service import calculate_balances
from app.services.split_service import calculate_user_global_summary

router = APIRouter()

@router.get("/groups/{group_id}/summary")
def group_balance_summary(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_balances(db, group_id)



@router.get("/my-summary/global")
def global_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_user_global_summary(db, current_user)