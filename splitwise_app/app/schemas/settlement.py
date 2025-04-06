from pydantic import BaseModel
from datetime import datetime

class SettlementCreate(BaseModel):
    group_id: int
    payee_id: int
    payer_id: int
    amount: float

class SettlementOut(SettlementCreate):
    id: int
    payer_id: int
    created_at: datetime

    class Config:
        orm_mode = True
