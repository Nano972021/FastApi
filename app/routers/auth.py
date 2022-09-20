from os import access
from ..schemas import Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, models, utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=["Authentication"])
# The user will provide his credentials; compare to what is stored in db
@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # get user with provided email; there is only one user
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Invalid Credentials")

    # verify password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token":access_token, "type":"bearer"}
