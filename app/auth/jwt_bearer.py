# the function of this file is to verify weather the request is verified or not
# verification of the protected route

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

        async def __call__(self, request: Request):
            credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).call(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(
                        status_code=403, details='Invalid or Expired Token!')
                return credentials.credentials
            else:
                raise HTTPException(
                    status_code=403, details='Invalid or Expired Token!')

    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid
