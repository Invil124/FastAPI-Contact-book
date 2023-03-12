from datetime import datetime

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.

    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts for a given user
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter_by(user_id=user.id).all()
    return contacts


async def get_contact(user, contact_id, db: Session):
    """
    The get_contact function takes in a user and contact_id, and returns the contact with that id.


    :param user: Filter the contacts by user
    :param contact_id: Find the contact in the database
    :param db: Session: Pass the database session to the function
    :return: A contact from the database
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id, user_id=user.id).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            user (User): The user who is creating the contact. This is used to associate contacts with users, and also for authorization purposes.

    :param body: ContactModel: Pass the data from the request body to the function
    :param user: User: Get the user id of the current logged in user
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(
        first_name=body.first_name,
        second_name=body.second_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_info=body.additional_info,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def patch_contact(body: ContactModel, user: User, contact_id: int, db: Session):
    """
    The patch_contact function takes in a ContactModel, User, int and Session.
    It then queries the database for a contact with the given id and user_id.
    If it finds one, it updates its first name, last name, email address phone number birthday and additional info to match those of the body parameter.
    Finally it commits these changes to the database.

    :param body: ContactModel: Get the contact information from the request body
    :param user: User: Check if the user is logged in
    :param contact_id: int: Find the contact in the database
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id, user_id=user.id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.second_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def delete_contact(contact_id: int, user: User, db: Session):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            user (User): The user who is deleting the contact. This is used for authorization purposes, so that only contacts belonging to this user can be deleted by them.
            db (Session): A connection to our database, which we use in order to query and update it with new data.

    :param contact_id: int: Get the contact with that id from the database
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id, user_id=user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_query(user: User, contact_first_name, contact_second_name, contact_email, db):
    """
    The get_contact_by_query function is used to query the database for a contact.
        The function takes in four parameters: user, contact_first_name, contact_second_name and db.
        It then queries the database using these parameters and returns a list of contacts that match the query.

    :param user: User: Get the user id from the user object
    :param contact_first_name: Filter the contacts by first name
    :param contact_second_name: Filter the query by second name
    :param contact_email: Filter the contacts by email
    :param db: Pass the database connection to the function
    :return: A list of contacts that match the search query
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(user_id=user.id)
    if contact_first_name:
        contact = contact.filter(Contact.first_name.like(contact_first_name)).all()
    elif contact_second_name:
        contact = contact.filter(Contact.second_name.like(contact_second_name)).all()
    elif contact_email:
        contact = contact.filter(Contact.email.like(contact_email)).all()

    return contact


async def get_nearest_birthday(user: User, db):
    """
    The get_nearest_birthday function takes a user and a database connection as arguments.
    It then queries the database for all contacts associated with that user, and returns
    a list of contacts whose birthday is within 7 days from today.

    :param user: User: Get the user id from the user object
    :param db: Pass the database connection to the function
    :return: A list of contacts whose birthday is within 7 days
    :doc-author: Trelent
    """
    date_now = datetime.now().date()
    birthday_7_days = []
    contacts = db.query(Contact).filter_by(user_id=user.id).all()

    for contact in contacts:
        contact_birthday = contact.birthday
        this_year_contact_birthday = datetime(date_now.year, contact_birthday.month, contact_birthday.day).date()
        days_left = this_year_contact_birthday - date_now
        if 0 <= days_left.days <= 7:
            birthday_7_days.append(contact)

    return birthday_7_days
