from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import repository.db as db
import bcrypt
import datetime
import jwt


class User(db.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def hash_password(self, password:str):
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password:str):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    def generate_token(self):
        expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        payload = {
            "sub": str(self.id),
            "exp": expiration,
        }
        return jwt.encode(payload, "    ", algorithm="HS256")
    

