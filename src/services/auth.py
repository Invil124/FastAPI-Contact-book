from typing import Optional
import pickle

import redis as redis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.repository import users as repository_users
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key_jwt
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    r = redis.Redis(host='localhost', port=6379, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. It then uses the pwd_context object to verify that the
        plain-text password matches the hashed one.

        :param self: Make the method call work on an instance of the class
        :param plain_password: Pass the password that is entered by the user
        :param hashed_password: Compare the password that is being entered with the hashed password stored in the database
        :return: A boolean value of true or false
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
        The hash is generated using the pwd_context object, which is an instance of Flask-Bcrypt's Bcrypt class.

        :param self: Represent the instance of the class
        :param password: str: Specify the password that will be hashed
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token.
            Args:
                data (dict): A dictionary containing the claims to be encoded in the JWT.
                expires_delta (Optional[float]): An optional parameter specifying how long, in seconds,
                    the access token should last before expiring. If not specified, it defaults to 15 minutes.

        :param self: Access the class attributes
        :param data: dict: Pass the data you want to encode into the token
        :param expires_delta: Optional[float]: Set the expiration time of the access token
        :return: A string of encoded data
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of seconds until the token expires, defaults to None.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: A refresh token that is encoded with the user's id and email
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=14)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
        It takes in a refresh_token as an argument and returns the username of the user who owns that token.
        If there is no such user, it raises an HTTPException with status code 400 (Bad Request) and detail 'Could not validate credentials'.


        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The username of the user who is making the request
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                username = payload['sub']
                return username
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token as an argument and returns the user
            object if it exists, otherwise it raises an exception.

        :param self: Access the class attributes
        :param token: str: Get the token from the header of a request
        :param db: Session: Get the database session
        :return: The user object from the database
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                username = payload["sub"]
                if username is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = self.r.get(f"user:{username}")
        if user is None:
            user = await repository_users.get_user_by_username(username, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{username}", pickle.dumps(user))
            self.r.expire(f"user:{username}", 900)
        else:
            user = pickle.loads(user)
        return user

    def create_email_token(self, data: dict):
        """
        The create_email_token function takes a dictionary of data and returns a token.
        The token is encoded with the SECRET_KEY, which is stored in the .env file.
        The algorithm used to encode the token is also stored in the .env file.

        :param self: Make the function a method of the user class
        :param data: dict: Pass in the data that will be encoded into a jwt
        :return: A token that is encoded with the user's email address and a secret key
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email associated with that token.
        It does this by decoding the JWT using our secret key, then checking to make sure that it has a scope of 'email_token'.
        If it does, we return the email address stored in its sub field. If not, we raise an HTTPException with status code 400
        and detail message &quot;Invalid scope for token&quot;. If there is any other error during decoding (such as if the signature is invalid),
        we raise another HTTPException with status code 422 and detail message &quot;Invalid token for email verification&quot;.

        :param self: Represent the instance of the class
        :param token: str: Pass the token that is sent to the user's email address
        :return: The email address that is associated with the token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'email_token':
                email = payload["sub"]
                return email
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid scope for token')

        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()
