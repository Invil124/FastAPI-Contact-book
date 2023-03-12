from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.connect import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET endpoint that returns the current user's information.
    It uses the auth_service to get the current user, and then returns it.

    :param current_user: User: Tell fastapi that the function will receive a user object
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The image file to be uploaded.
            current_user (User): The currently logged in user.  This is passed by the auth_service dependency, which uses JWT tokens to authenticate users and pass their information into this function as an argument.  It's used here so that we can update only the avatar of the currently logged in user, not any other users' avatars!
            db (Session): A database session object provided by FastAPI's Depends() method, which allows us to access our database from

    :param file: UploadFile: Get the file uploaded by the user
    :param current_user: User: Get the current user's email
    :param db: Session: Get the database session
    :return: The user object
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill')
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
