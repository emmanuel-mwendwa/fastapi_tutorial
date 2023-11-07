from passlib.context import CryptContext

# what hashing algorithm we want to use 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)