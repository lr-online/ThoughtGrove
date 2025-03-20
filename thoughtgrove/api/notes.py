from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status

from thoughtgrove.models.note import Note, NoteCreate, NoteUpdate, NoteInDB
from thoughtgrove.models.user import User
from thoughtgrove.crud.note import (
    create_note, 
    get_note, 
    update_note, 
    delete_note, 
    get_notes_by_user
)
from thoughtgrove.core.deps import get_current_user
from thoughtgrove.db.mongodb import mongodb

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note_api(
    note_in: NoteCreate,
    current_user: User = Depends(get_current_user)
):
    """创建笔记"""
    # 使用当前用户ID
    note_in.user_id = current_user.id
    
    try:
        db = mongodb.get_database()
        note = await create_note(db, note_in)
        return note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建笔记失败: {str(e)}"
        )


@router.get("/{note_id}", response_model=Note)
async def read_note(
    note_id: str = Path(..., title="笔记ID"),
    current_user: User = Depends(get_current_user)
):
    """获取笔记详情"""
    db = mongodb.get_database()
    note = await get_note(db, note_id)
    
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="笔记不存在"
        )
    
    # 验证笔记所有权
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问此笔记"
        )
    
    return note


@router.put("/{note_id}", response_model=Note)
async def update_note_api(
    note_update: NoteUpdate,
    note_id: str = Path(..., title="笔记ID"),
    current_user: User = Depends(get_current_user)
):
    """更新笔记"""
    db = mongodb.get_database()
    note = await get_note(db, note_id)
    
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="笔记不存在"
        )
    
    # 验证笔记所有权
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此笔记"
        )
    
    updated_note = await update_note(db, note_id, note_update)
    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_api(
    note_id: str = Path(..., title="笔记ID"),
    current_user: User = Depends(get_current_user)
):
    """删除笔记"""
    db = mongodb.get_database()
    note = await get_note(db, note_id)
    
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="笔记不存在"
        )
    
    # 验证笔记所有权
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此笔记"
        )
    
    result = await delete_note(db, note_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除笔记失败"
        )


@router.get("/", response_model=List[Note])
async def read_user_notes(
    skip: int = Query(0, ge=0, title="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, title="返回记录数"),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有笔记"""
    db = mongodb.get_database()
    notes = await get_notes_by_user(db, current_user.id, skip, limit)
    return notes 