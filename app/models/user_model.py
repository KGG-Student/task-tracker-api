from app.database import db

users_collection = db["users"]

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)
