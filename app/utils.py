import re
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_passowd):
    # First: hash provided password 
    # Then: compared to the hashed password stored in the database
    return pwd_context.verify(plain_password, hashed_passowd) # it does all that 