import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    patch_contact,
    delete_contact,
    get_nearest_birthday
)


class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            first_name="test",
            second_name="test_second_name",
            email="test@email.com",
            phone_number="1234567891",
            birthday=datetime(2020, 5, 17),
            additional_info="test_add_info"
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.second_name, body.second_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional_info, body.additional_info)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(
            first_name="test",
            second_name="test_second_name",
            email="test@email.com",
            phone_number="1234567891",
            birthday=datetime(2020, 5, 17),
            additional_info="test_add_info"
        )
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        self.session.commit.return_value = None
        result = await patch_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(
            first_name="test",
            second_name="test_second_name",
            email="test@email.com",
            phone_number="1234567891",
            birthday=datetime(2020, 5, 17),
            additional_info="test_add_info"
        )
        self.session.query().filter_by().first.return_value = None
        self.session.commit.return_value = None
        result = await patch_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_nearest_birthday(self):
        contacts = [Contact(birthday=datetime.now() + timedelta(days=1)),
                    Contact(birthday=datetime.now() + timedelta(days=2)),
                    Contact(birthday=datetime.now() + timedelta(days=3)),
                    Contact(birthday=datetime.now() + timedelta(days=6)),
                    Contact(birthday=datetime.now() + timedelta(days=14)),
                    ]
        self.session.query().filter_by().all.return_value = contacts
        result = await get_nearest_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts[0:4]) # тільки у 4 з 5 контактів день народження у межах 7 днів у 5 ні.


if __name__ == '__main__':
    unittest.main()
