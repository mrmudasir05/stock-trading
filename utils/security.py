from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Database.db import get_db
from models.user import User
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password helpers
def hash_password(password: str) -> str:
    """

    :param password: password of the user
    :return: hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """

    :param plain_password: password
    :param hashed_password: hashed password
    :return: True, False
    """
    return pwd_context.verify(plain_password, hashed_password)


# JWT helpers
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """

    :param data: data of the user
    :param expires_delta: time of expiring the token
    :return: jwt token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str,str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # same as your login route


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """

    :param token: token for the logged in user
    :param db: session for the database
    :return: object for the user if found else None
    """

    payload = decode_token(token)
    id: int = payload.get("sub")
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


def master_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> None:
    """

    :param token:  token for the user whose id = 1
    :param db: session for database
    :return: object for the user if found else None
    """
    payload = decode_token(token)
    user_id = int(payload["sub"])  # get user id from token
    if user_id != 1:  # Only master user allowed
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only master user can perform this action"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


