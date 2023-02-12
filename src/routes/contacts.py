from datetime import datetime
from typing import List

from fastapi import Path, Depends, HTTPException, status, APIRouter

from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.schemas import ContactModel, RespondsContact
from src.repository import contacts as contact_repository

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[RespondsContact])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await contact_repository.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=RespondsContact)
async def find_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await contact_repository.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/find/", response_model=List[RespondsContact])
async def find_contact_by_query(contact_first_name: str = None, contact_second_name: str = None,
                                contact_email: str = None, db: Session = Depends(get_db)):
    contact = await contact_repository.get_contact_by_query(contact_first_name, contact_second_name, contact_email, db)
    print(contact)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/birthday/", response_model=List[RespondsContact])
async def get_nearest_birthday(db: Session = Depends(get_db)):
    contacts = await contact_repository.get_nearest_birthday(db)
    return contacts


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=RespondsContact)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await contact_repository.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=RespondsContact)
async def update_contact(body: ContactModel, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await contact_repository.patch_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await contact_repository.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact