from typing import Optional
from bson import ObjectId
from thoughtgrove.db.mongodb import mongodb
from thoughtgrove.models.user import UserCreate, UserInDB, UserUpdate
from thoughtgrove.core.security import get_password_hash

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    user_dict = await mongodb.db.users.find_one({"email": email})
    if user_dict:
        user_dict["id"] = str(user_dict.pop("_id"))
        return UserInDB(**user_dict)
    return None

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    try:
        user_dict = await mongodb.db.users.find_one({"_id": ObjectId(user_id)})
        if user_dict:
            user_dict["id"] = str(user_dict.pop("_id"))
            return UserInDB(**user_dict)
        return None
    except:
        return None

async def create_user(user: UserCreate) -> UserInDB:
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    result = await mongodb.db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return UserInDB(**user_dict)

async def update_user(user_id: str, user: UserUpdate) -> Optional[UserInDB]:
    user_dict = user.model_dump(exclude_unset=True)
    if "password" in user_dict:
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    
    if user_dict:
        await mongodb.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_dict}
        )
    return await get_user_by_id(user_id)

async def delete_user(user_id: str) -> bool:
    result = await mongodb.db.users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0 