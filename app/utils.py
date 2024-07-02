from . import oauth2
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)

def password_hash(password):
    return pwd_context.hash(password)