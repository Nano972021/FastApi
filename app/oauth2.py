from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# to generate a token we need: 
# Secert Key, which is a long string, to generate a signature
# Algorithm to encode payload
# Payload, which is the data passed to the encode algorithm
# Expire Date;to put a limitation on how long the user is logged in

SECERT_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Create access token
def create_access_token(data: dict):
    to_encode = data.copy() # to not miss with the original data
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # 30 minutes from logging in - COOL!
    to_encode.update({"exp":expire}) # add expiration time to payload

    encoded_jwt = jwt.encode(to_encode, SECERT_KEY, algorithm=[ALGORITHM]) # ACCESS TOKEN
    return encoded_jwt


def verify_access_token(token, credential_exception):
    
    try:
        #decode token
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        #get current user's ID
        id: str = payload.get("user_id")
        if not id:
            raise credential_exception
        
        # validate ID
        token_data = TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                                        detail="Invalid Credentials",
                                                        headers={"WWW-Authenticate":"Bearer"})

    return verify_access_token(token, credential_exception)