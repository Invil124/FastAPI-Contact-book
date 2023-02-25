from datetime import datetime

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session):
    contacts = db.query(Contact).filter_by(user_id=user.id).all()
    return contacts


async def get_contact(user, contact_id, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id, user_id=user.id).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
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


async def patch_contact(body: ContactModel,user: User, contact_id: int, db: Session):
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
    contact = db.query(Contact).filter_by(id=contact_id, user_id=user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_query(user: User, contact_first_name, contact_second_name, contact_email, db):
    contact = db.query(Contact).filter_by(user_id=user.id)
    if contact_first_name:
        contact = contact.filter(Contact.first_name.like(contact_first_name)).all()
    elif contact_second_name:
        contact = contact.filter(Contact.second_name.like(contact_second_name)).all()
    elif contact_email:
        contact = contact.filter(Contact.email.like(contact_email)).all()

    return contact


async def get_nearest_birthday(user: User, db):
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
