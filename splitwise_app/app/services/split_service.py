from sqlalchemy.orm import Session
from app.db.models.expense import Expense
from app.db.models.group import Group
from collections import defaultdict
from app.db.models.settlement import Settlement
from app.db.models.user import User


def calculate_balances(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return []

    expenses = group.expenses
    members = group.members
    num_members = len(members)
    balances = defaultdict(float)

    # Expense logic
    for expense in expenses:
        print(f"Expense {expense.id}: split_type={expense.split_type}")
        split_type = expense.split_type or "equal"  # <-- fallback if missing

        if split_type == "equal":
            print("✅ Equal logic triggered")
            share = expense.amount / num_members
            for member in members:
                if member.id == expense.payer_id:
                    balances[member.id] += expense.amount - share
                else:
                    balances[member.id] -= share

        elif split_type == "unequal":
            print("✅ Unequal logic triggered")
            shares = expense.split_details or {}
            for user_id, amount in shares.items():
                user_id = int(user_id)  # Ensure int keys
                amount = float(amount)
                if user_id == expense.payer_id:
                    balances[user_id] += expense.amount - amount
                else:
                    balances[user_id] -= amount

        elif split_type == "percentage":
            print("✅ Percentage logic triggered")
            shares = expense.split_details or {}
            for user_id, percent in shares.items():
                user_id = int(user_id)
                share_amount = (percent / 100.0) * expense.amount
                if user_id == expense.payer_id:
                    balances[user_id] += expense.amount - share_amount
                else:
                    balances[user_id] -= share_amount

    # Settlement logic
    settlements = db.query(Settlement).filter(Settlement.group_id == group_id).all()
    # for s in settlements:
        # balances[s.payer_id] -= s.amount
        # balances[s.payee_id] += s.amount

    for s in settlements:
        balances[s.payer_id] += s.amount   # payer owes less
        balances[s.payee_id] -= s.amount   # payee is owed less


    # Return list of usernames with balances
    result = []
    for member in members:
        result.append({
            "user": member.username,
            "balance": round(balances[member.id], 2)
        })

    return result


def calculate_user_global_summary(db: Session, current_user: User):
    you_owe = []
    you_are_owed = []

    for group in current_user.groups:
        expenses = group.expenses
        members = group.members
        balances = defaultdict(float)
        num_members = len(members)

        for expense in expenses:
            share = expense.amount / num_members
            for member in members:
                if member.id == expense.payer_id:
                    balances[member.id] += expense.amount - share
                else:
                    balances[member.id] -= share

        settlements = db.query(Settlement).filter(Settlement.group_id == group.id).all()
        for s in settlements:
            balances[s.payer_id] += s.amount   # 🟢 Payer owes less
            balances[s.payee_id] -= s.amount 

        current_balance = balances[current_user.id]

        for member in members:
            if member.id == current_user.id:
                continue
            if current_balance < 0 and balances[member.id] > 0:
                you_owe.append({
                    "to": member.username,
                    "amount": round(-current_balance, 2),
                    "group": group.name
                })
            elif current_balance > 0 and balances[member.id] < 0:
                you_are_owed.append({
                    "from": member.username,
                    "amount": round(current_balance, 2),
                    "group": group.name
                })

    return {
        "you_owe": you_owe,
        "you_are_owed": you_are_owed,
        "settled": len(you_owe) == 0 and len(you_are_owed) == 0
    }
