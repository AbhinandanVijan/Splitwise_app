from sqlalchemy.orm import Session
from app.schemas.expense import ExpenseCreate
from app.db.models.expense import Expense
from app.db.models.user import User

def create_expense(db: Session, expense_in: ExpenseCreate, payer: User) -> Expense:
    expense = Expense(
        amount=expense_in.amount,
        description=expense_in.description,
        group_id=expense_in.group_id,
        payer_id=payer.id,
        split_type=expense_in.split_type.value,
        split_details=expense_in.split_details,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses_for_group(db: Session, group_id: int):
    return db.query(Expense).filter(Expense.group_id == group_id).all()
