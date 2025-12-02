from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from auth.deps import get_current_user
from groups import schemas
from groups import repository as group_repo
from users.repository import get_user_by_id

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/", response_model=schemas.GroupOut)
def create_group(group_in: schemas.GroupCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = group_repo.create_group(db, name=group_in.name, owner_id=current_user.id)
    return group

@router.get("/my-groups", response_model=list[schemas.GroupOut])
def my_groups(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    groups = group_repo.get_groups_for_user(db, current_user.id)
    return groups

@router.get("/{group_id}", response_model=schemas.GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    # check membership
    member = db.query(type(group).members.property.mapper.class_).filter_by(group_id=group_id, user_id=current_user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No perteneces a este grupo")
    return group

@router.post("/{group_id}/members", response_model=schemas.MemberOut)
def add_member(group_id: int, member_in: schemas.MemberAdd, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # only admin can add
    if not group_repo.is_admin(db, group_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo admin puede agregar miembros")
    # verify user exists
    user = get_user_by_id(db, member_in.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    member = group_repo.add_member(db, group_id=group_id, user_id=member_in.user_id, role=member_in.role)
    return member

@router.get("/{group_id}/members", response_model=list[schemas.MemberOut])
def list_members(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # only members can list
    ms = group_repo.list_members(db, group_id)
    # check membership
    if not any(m.user_id == current_user.id for m in ms):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No perteneces a este grupo")
    return ms
