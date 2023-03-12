from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_username(username: str, db: Session) -> User:
    """
    The get_user_by_username function takes a username and returns the user with that username.

    :param username: str: Specify the username of the user we want to get from our database
    :param db: Session: Pass the database session to the function
    :return: The first user object in the database that matches the username
    :doc-author: Trelent
    """
    return db.query(User).filter(User.username == username).first()


async def get_user_by_email(email, db):
    """
    The get_user_by_email function takes in an email and a database connection,
    and returns the first user with that email address. If no such user exists,
    it returns None.

    :param email: Filter the query to find a specific user
    :param db: Connect to the database
    :return: The first user with a matching email
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the username, email, and password of the new user.
            db (Session): The SQLAlchemy Session object used to query and modify data in our database.

    :param body: UserModel: Specify the type of data that is expected to be passed in
    :param db: Session: Pass the database session to the function
    :return: The newly created user
    :doc-author: Trelent
    """
    new_user = User(
        username=body.username,
        email=body.email,
        password=body.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user in the database
    :param token: str | None: Update the refresh token in the database
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that will be passed into the function
    :param db: Session: Pass in the database session
    :return: The updated user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
