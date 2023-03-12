from datetime import datetime
from typing import List

from fastapi import Path, Depends, HTTPException, status, APIRouter
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.schemas import ContactModel, RespondsContact
from src.repository import contacts as contact_repository
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[RespondsContact])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await contact_repository.get_contacts(current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=RespondsContact)
async def find_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contact function is used to find a contact by its id.

    :param contact_id: int: Get the contact id from the url
    :param ge: Set a minimum value for the contact_id parameter
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await contact_repository.get_contact(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/find/", response_model=List[RespondsContact])
async def find_contact_by_query(contact_first_name: str = None, contact_second_name: str = None,
                                contact_email: str = None, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contact_by_query function is used to find a contact by their first name, second name or email.
        The function takes in the following parameters:
            - contact_first_name (str): The first name of the user you are searching for.
            - contact_second_name (str): The second name of the user you are searching for.
            - contact_email (str): The email address of the user you are searching for.

    :param contact_first_name: str: Specify the first name of a contact
    :param contact_second_name: str: Specify the second name of a contact
    :param contact_email: str: Search for a contact by email
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await contact_repository.get_contact_by_query(current_user, contact_first_name, contact_second_name,
                                                            contact_email, db)
    print(contact)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/birthday/", response_model=List[RespondsContact])
async def get_nearest_birthday(db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_nearest_birthday function returns the nearest birthday of a contact.
        The function takes in two parameters: db and current_user.
        The db parameter is used to connect to the database, while current_user is used for authentication purposes.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contacts with the nearest birthday
    :doc-author: Trelent
    """
    contacts = await contact_repository.get_nearest_birthday(current_user, db)
    return contacts


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=RespondsContact,
             description='No more than 3 requests per minute',
             dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Create a new contact
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await contact_repository.create_contact(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=RespondsContact)
async def update_contact(body: ContactModel, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, and returns the updated contact.
        If no contact is found with that id, it raises an HTTPException.

    :param body: ContactModel: Pass in the contact model that will be used to update the contact
    :param contact_id: int: Get the contact_id from the path
    :param ge: Specify the minimum value of the path parameter
    :param db: Session: Access the database
    :param current_user: User: Get the user_id of the current user
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await contact_repository.patch_contact(body, current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
        The function takes in an integer representing the id of the contact to be deleted,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the contact id to be deleted
    :param ge: Specify that the path parameter must be greater than or equal to 1
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await contact_repository.delete_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact
