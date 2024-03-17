import repository.db as db
import model.saved_file as SF
from model.user import User
from schema.user_schema import UserCreate, UserLogin, Token

from fastapi import  HTTPException, status, BackgroundTasks, APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(db.get_db)):
    user = User(username=user_data.username)
    user.hash_password(user_data.password)
    db.add(user)
    db.commit()
    return {"message": "User has been created"}


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(db.get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, default="Invalid Credentials")
    token = user.generate_token()
    return Token(access_token=token, token_type="bearer")