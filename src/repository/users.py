from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_username(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username).first()


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.username == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    new_user = User(
        username=body.username,
        email=body.email,
        password=body.password1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
