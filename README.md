# Task Tracker API

A backend web service built with FastAPI for managing tasks, authentication, and project tracking.
Developed for ITCC14 Web Services Final Project.

## Team Members
- Mychal Redoblado (@Ka1ma) (MychalXU)
- Kyle Gabriel T. Galanida (KGG-Student)
- Karlos Semilla (@Ykarlossemilla)
- Jhemar Visande (@JhemarVisande)

## Project Overview

### Problem Statement
Teams and individuals often struggle to track their daily tasks effectively. This API aims to provide a lightweight system to manage tasks, monitor progress, and maintain accountability.

### Goals
- Implement a secure authentication system using JWT
- Provide CRUD operations for task management
- Ensure a simple and reliable backend for future frontend integration

## API Documentation

### Authentication Endpoints

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password"
}
```

#### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Task Endpoints

All task endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

#### Create Task
```
POST /api/tasks/
Content-Type: application/json

{
  "title": "Task Title",
  "description": "Task description",
  "completed": false,
  "due_date": "2024-12-31"
}
```

#### List Tasks
```
GET /api/tasks/
```

Response:
```json
{
  "tasks": [
    {
      "id": "task_id",
      "title": "Task Title",
      "description": "Task description",
      "completed": false,
      "due_date": "2024-12-31",
      "owner_email": "user@example.com",
      "created_at": "2024-11-15T10:00:00"
    }
  ]
}
```

#### Get Task Details
```
GET /api/tasks/{task_id}
```

#### Update Task
```
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "completed": true
}
```

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Ka1ma/Assignment-Task-Tracker-API.git
cd task-tracker-api
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
MONGODB_URL=mongodb://localhost:27017/tasktracker
SECRET_KEY=your_secret_key_here
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Testing

Run the test suite:
```bash
pytest tests/test_api.py -v
```

## Project Milestones

### Milestone 1 (Nov Week 1): Project Setup and API Design ✅
- Updated README.md with project overview and problem statement
- Created FastAPI project structure and virtual environment
- Added initial routes and data models

### Milestone 2 (Nov Week 2): Authentication and Database Integration ✅
- Working register and login endpoints
- MongoDB connection established
- Token-based authentication implemented

### Milestone 3 (Nov Week 3): Task CRUD Operations ✅
- CRUD endpoints for tasks
- Middleware for authentication
- Test cases for each route

### Milestone 4 (Nov Week 4): Testing and Deployment
- Passing tests ✅
- Hosted API link (pending deployment)
- Final README documentation ✅

### Milestone 5 (Dec Week 1): Final Presentation and Documentation
- Presentation slides
- API documentation ✅
- Summary of lessons learned

## Repository
https://github.com/Ka1ma/Assignment-Task-Tracker-API
