import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

from private import password

os.environ.get('DATABASE_URL', f'postgresql://postgres:{password}@localhost:5432/warbler-tests')

from app import app

db.create_all()


class UserTestCase(TestCase):

    def setUp(self):
        
        db.drop_all()
        db.create_all()

        u.id = self.uid
        u.id = 500
        u = User.signup("test", "123@123.com", "123123", None)
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        answer = super().tearDown()
        db.session.rollback()
        return answer

    def test_msg(self):
        msg = Message(
            text="test",
            user_id=self.uid
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test")

    def test_msg_likes(self):
        msg1 = Message(
            text="test",
            user_id=self.uid
        )

        msg2 = Message(
            text="testy2",
            user_id=self.uid 
        )

        u = User.signup("username1", "456@123.com", "456456", None)
        uid = 888
        u.id = uid
        db.session.add_all([msg1, msg2, u])
        db.session.commit()

        u.likes.append(msg1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, msg1.id)


        