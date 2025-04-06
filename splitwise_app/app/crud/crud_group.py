from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate
from app.db.models.group import Group
from app.db.models.user import User

def create_group(db: Session, group_in: GroupCreate) -> Group:
    group = Group(name=group_in.name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def get_groups(db: Session):
    return db.query(Group).all()


def add_user_to_group(db: Session, group_id: int, user: User):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return None
    if user not in group.members:
        group.members.append(user)
        db.commit()
        db.refresh(group)
    return group


def get_group_members(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return None
    return group.members

