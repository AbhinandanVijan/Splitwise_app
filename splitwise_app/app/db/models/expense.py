from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from sqlalchemy import JSON

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    payer_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    payer = relationship("User", back_populates="expenses_paid")
    group = relationship("Group", back_populates="expenses")


    split_type = Column(String, default="equal")  # equal/unequal/percentage
    split_details = Column(JSON, nullable=True)   # stores dict of splits


   



