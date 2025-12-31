from fastapi import APIRouter, Depends, HTTPException, status
from src.models import UserModel
from src.database import get_db
from src.auth import get_password_hash, verify_password, create_access_token, get_current_user
from pydantic import BaseModel

router = APIRouter()

class AuthRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(req: AuthRequest):
    db = get_db()
    existing_user = await db.users.find_one({"username": req.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(req.password)
    user_dict = {
        "username": req.username,
        "password": hashed_password,
        "totalTokens": 0,
        "chatCount": 0,
        "createdAt": None # Will be set by MongoDB or Pydantic if handled there
    }
    
    result = await db.users.insert_one(user_dict)
    token = create_access_token({"_id": str(result.inserted_id)})
    
    return {"user": {"username": req.username}, "token": token}

@router.post("/login")
async def login(req: AuthRequest):
    db = get_db()
    user = await db.users.find_one({"username": req.username})
    
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid login credentials")
    
    token = create_access_token({"_id": str(user["_id"])})
    
    return {
        "user": {
            "username": user["username"],
            "chatCount": user.get("chatCount", 0),
            "totalTokens": user.get("totalTokens", 0)
        },
        "token": token
    }

@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "chatCount": user.get("chatCount", 0),
        "totalTokens": user.get("totalTokens", 0)
    }
