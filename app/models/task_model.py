from app.database import db
from datetime import datetime, date
from bson import ObjectId

tasks_collection = db["tasks"]

async def create_task(task_data: dict):
    # Convert date string to datetime object if present
    if "due_date" in task_data and task_data["due_date"]:
        if isinstance(task_data["due_date"], str):
            try:
                # Convert to datetime object
                task_data["due_date"] = datetime.strptime(task_data["due_date"], "%Y-%m-%d")
            except ValueError:
                # If date parsing fails, remove the due_date
                del task_data["due_date"]
        elif isinstance(task_data["due_date"], date):
            # Convert date object to datetime object
            task_data["due_date"] = datetime.combine(task_data["due_date"], datetime.min.time())
    
    task_data["created_at"] = datetime.utcnow()
    result = await tasks_collection.insert_one(task_data)
    return str(result.inserted_id)

async def get_tasks_by_owner(email: str):
    tasks = await tasks_collection.find({"owner_email": email}).to_list(100)
    for t in tasks:
        t["id"] = str(t["_id"])
        del t["_id"]
    return tasks

async def update_task(task_id: str, data: dict, owner_email: str):
    # Convert date string to datetime object if present
    if "due_date" in data and data["due_date"]:
        if isinstance(data["due_date"], str):
            try:
                # Convert to datetime object
                data["due_date"] = datetime.strptime(data["due_date"], "%Y-%m-%d")
            except ValueError:
                # If date parsing fails, remove the due_date
                del data["due_date"]
        elif isinstance(data["due_date"], date):
            # Convert date object to datetime object
            data["due_date"] = datetime.combine(data["due_date"], datetime.min.time())
    
    result = await tasks_collection.update_one(
        {"_id": ObjectId(task_id), "owner_email": owner_email},
        {"$set": data}
    )
    return result.modified_count > 0

async def delete_task(task_id: str, owner_email: str):
    result = await tasks_collection.delete_one(
        {"_id": ObjectId(task_id), "owner_email": owner_email}
    )
    return result.deleted_count > 0
