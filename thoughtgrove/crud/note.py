from datetime import datetime, UTC
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from thoughtgrove.models.note import NoteCreate, NoteUpdate, NoteInDB


async def create_note(db: AsyncIOMotorDatabase, note_in: NoteCreate) -> NoteInDB:
    """创建笔记"""
    now = datetime.now(UTC)
    note_dict = note_in.model_dump()
    note_dict.update({
        "created_at": now,
        "updated_at": now
    })
    
    try:
        result = await db.notes.insert_one(note_dict)
        # 获取新创建的笔记
        note_dict["_id"] = str(result.inserted_id)
        return NoteInDB(**note_dict)
    except PyMongoError as e:
        # 记录错误并返回None
        print(f"创建笔记时发生错误: {str(e)}")
        raise


async def get_note(db: AsyncIOMotorDatabase, note_id: str) -> Optional[NoteInDB]:
    """通过ID获取笔记"""
    try:
        note = await db.notes.find_one({"_id": ObjectId(note_id)})
        if note:
            note["_id"] = str(note["_id"])
            return NoteInDB(**note)
        return None
    except PyMongoError as e:
        print(f"获取笔记时发生错误: {str(e)}")
        return None


async def update_note(
    db: AsyncIOMotorDatabase, 
    note_id: str, 
    note_update: NoteUpdate
) -> Optional[NoteInDB]:
    """更新笔记"""
    now = datetime.now(UTC)
    update_data = note_update.model_dump(exclude_unset=True)
    
    if not update_data:
        # 没有需要更新的字段
        note = await get_note(db, note_id)
        return note
    
    update_data["updated_at"] = now
    
    try:
        await db.notes.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": update_data}
        )
        return await get_note(db, note_id)
    except PyMongoError as e:
        print(f"更新笔记时发生错误: {str(e)}")
        return None


async def delete_note(db: AsyncIOMotorDatabase, note_id: str) -> bool:
    """删除笔记"""
    try:
        result = await db.notes.delete_one({"_id": ObjectId(note_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"删除笔记时发生错误: {str(e)}")
        return False


async def get_notes_by_user(
    db: AsyncIOMotorDatabase, 
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[NoteInDB]:
    """获取用户所有笔记"""
    try:
        notes = []
        cursor = db.notes.find({"user_id": user_id}).skip(skip).limit(limit).sort("created_at", -1)
        
        async for note in cursor:
            note["_id"] = str(note["_id"])
            notes.append(NoteInDB(**note))
            
        return notes
    except PyMongoError as e:
        print(f"获取用户笔记时发生错误: {str(e)}")
        return [] 