from app.schemas.settlement import SettlementCreate, SettlementOut
from app.crud.crud_settlement import record_settlement
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.db.models.user import User

router = APIRouter()

@router.post("/settle_up", response_model=SettlementOut)
def settle_up(
    settlement_in: SettlementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return record_settlement(db, settlement_in, current_user)
