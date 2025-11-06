from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.models.user_model import get_user_by_email, create_user
from app.utils.hashing import hash_password, verify_password
from app.utils.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = {"email": user.email, "username": user.username, "password": hashed_pw}
    user_id = await create_user(new_user)
    return {"id": user_id, "email": user.email, "username": user.username}

@router.post("/login")
async def login_user(credentials: UserLogin):
    user = await get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
