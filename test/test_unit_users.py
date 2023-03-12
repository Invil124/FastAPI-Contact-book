import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_username,
    get_user_by_email,
    create_user,
    update_avatar
    )


class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_username(self):
        user = User(username="Test")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_username(username=user.username, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_username_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_username(username="test", db=self.session)
        self.assertIsNone(result)

    async def test_get_user_by_email(self):
        user = User(email="test_email")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="test", db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = UserModel(
            username="test123",
            email="test@email.com",
            password="12345678",
        )
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_avatar(self):
        user = User(email="test")
        self.session.query().filter().first.return_value = user
        result = await update_avatar(user.email, "avatar_url", self.session)
        self.assertEqual(result.avatar, user.avatar)


if __name__ == '__main__':
    unittest.main()
