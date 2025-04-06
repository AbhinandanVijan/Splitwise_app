from sqlalchemy.orm import Session
from app.schemas.settlement import SettlementCreate
from app.db.models.settlement import Settlement
from app.db.models.user import User

def record_settlement(db: Session, settlement_in: SettlementCreate, currentUser: User) -> Settlement:
    settlement = Settlement(
        group_id=settlement_in.group_id,
        payee_id=settlement_in.payee_id,
        amount=settlement_in.amount,
        payer_id=settlement_in.payer_id,
    )
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement
