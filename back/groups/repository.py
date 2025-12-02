from sqlalchemy.orm import Session
from .models_sql import Group, GroupMember

def create_group(db: Session, name: str, owner_id: int):
    group = Group(name=name, created_by=owner_id)
    db.add(group)
    db.commit()
    db.refresh(group)
    # add owner as member admin
    member = GroupMember(group_id=group.id, user_id=owner_id, role="admin")
    db.add(member)
    db.commit()
    db.refresh(member)
    return group

def get_groups_for_user(db: Session, user_id: int):
    return db.query(Group).join(GroupMember).filter(GroupMember.user_id == user_id).all()

def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()

def add_member(db: Session, group_id: int, user_id: int, role: str = "member"):
    # prevent duplicates
    existing = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id).first()
    if existing:
        return existing
    member = GroupMember(group_id=group_id, user_id=user_id, role=role)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def list_members(db: Session, group_id: int):
    return db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

def is_admin(db: Session, group_id: int, user_id: int):
    m = db.query(GroupMember).filter(GroupMember.group_id==group_id, GroupMember.user_id==user_id, GroupMember.role=="admin").first()
    return bool(m)
