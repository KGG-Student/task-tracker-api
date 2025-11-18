from fastapi import FastAPI
from app.routes import auth_routes, task_routes

app = FastAPI()
app.include_router(auth_routes.router, prefix='/api/auth')
app.include_router(task_routes.router, prefix='/api/tasks')
