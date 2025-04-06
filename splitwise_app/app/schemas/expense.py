from pydantic import BaseModel
from pydantic import BaseModel, model_validator, validator
from datetime import datetime
from typing import Optional, Dict
from enum import Enum


class ExpenseBase(BaseModel):
    amount: float
    description: str
    group_id: int

class ExpenseOut(ExpenseBase):
    id: int
    payer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SplitType(str, Enum):
    equal = "equal"
    unequal = "unequal"
    percentage = "percentage"

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    group_id: int
    split_type: SplitType
    split_details: Optional[Dict[int, float]] = None  # user_id -> value (amount or %)

    @validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @model_validator(mode="after")
    def validate_split_logic(self):
        split_type = self.split_type
        split_details = self.split_details or {}

        if split_type == SplitType.unequal:
            total = sum(split_details.values())
            if round(total, 2) != round(self.amount, 2):
                raise ValueError(f"Unequal split total ({total}) must equal amount ({self.amount})")

        elif split_type == SplitType.percentage:
            total = sum(split_details.values())
            if round(total, 2) != 100.0:
                raise ValueError("Percentage split must total 100")

        elif split_type == SplitType.equal:
            if self.split_details:
                raise ValueError("Equal split should not include split_details")

        return self