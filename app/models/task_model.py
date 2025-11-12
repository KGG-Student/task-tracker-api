from app.database import db
from datetime import datetime

tasks_collection = db["tasks"]

async def create_task(task_data: dict):
    task_data["created_at"] = datetime.utcnow()
    result = await tasks_collection.insert_one(task_data)
    return str(result.inserted_id)

async def get_tasks_by_owner(email: str):
    tasks = await tasks_collection.find({"owner_email": email}).to_list(100)
    for t in tasks:
        t["id"] = str(t["_id"])
    return tasks

async def update_task(task_id: str, data: dict, owner_email: str):
    result = await tasks_collection.update_one(
        {"_id": {"$oid": task_id}, "owner_email": owner_email},
        {"$set": data}
    )
    return result.modified_count > 0

async def delete_task(task_id: str, owner_email: str):
    result = await tasks_collection.delete_one(
        {"_id": {"$oid": task_id}, "owner_email": owner_email}
    )
    return result.deleted_count > 0
