from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base 
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    groups = relationship("Group", secondary="group_members", back_populates="members")
    expenses_paid = relationship("Expense", back_populates="payer")

