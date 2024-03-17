from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from fastapi import Depends, HTTPException
# from model.bearer import JWTBearer
# from model.user import User
# import jwt

engine = create_engine("sqlite:///xx.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_current_user(token: str = Depends(JWTBearer())) -> User:
#     try:
#         payload = jwt.decode(token, "MY_SECRET_KEY", algorithms=["HS256"])
#         user_id = payload.get('sub')
#         db = SessionLocal()
#         return db.query(User).filter(User.id==user_id).first()
#     except(jwt.PyJWTError, AttributeError):
#         return HTTPException(status_code="403", detail="Error decoding token")