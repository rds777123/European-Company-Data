from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.database import get_db
from backend.models import User
from backend.schemas import UserCreate, UserOut, APIResponse

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=APIResponse[UserOut])
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(
        username=payload.username,
        hashed_password=pwd_context.hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return APIResponse(data=UserOut.model_validate(user))


@router.get("/{user_id}", response_model=APIResponse[UserOut])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(data=UserOut.model_validate(user))
