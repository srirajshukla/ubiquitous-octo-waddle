from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool=True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials : HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request=request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        
    def verify_jwt(self, jwttoken: str) -> bool:
        isTokenVaid = False

        try: 
            payload = decodeJWT(jwttoken)
        except:
            payload = None
        if payload:
            isTokenVaid = True
        return isTokenVaid
    


import jwt
import time

def decodeJWT(jwttoken):
    decoded = jwt.decode(jwttoken, "MY_SECRET_KEY", algorithms=["HS256"])
    return decoded if decoded['exp'] >= time.time() else None