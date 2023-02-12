from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    second_name = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone_number = Column(String(100), nullable=False, unique=True)
    birthday = Column(Date, nullable=False)
    additional_info = Column(Text, nullable=True)
