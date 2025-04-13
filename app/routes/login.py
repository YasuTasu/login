from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, User
from app.auth import verify_password, create_access_token
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()

class UserLogin(BaseModel):
    user_id: str
    password: str
    role: str  # ✅ ロール（user/admin）を追加

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # ✅ ユーザーの `role` をチェック
    if user.role == "admin" and db_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin permission required")

    # ✅ JWT トークンに `role` も含める
    access_token = create_access_token(data={"sub": db_user.user_id, "role": db_user.role}, expires_delta=timedelta(minutes=30))
    
    return {"access_token": access_token, "token_type": "bearer", "role": db_user.role}
