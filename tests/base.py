import unittest

from flask import url_for

from blog import create_app
from blog.extensions import db
from blog.models import  Admin


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('test')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

        db.create_all()
        username = 'echocho'; email = 'echo@email.com'; password='123'
        hashed = Admin().hash_password(password)
        user = Admin(username=username, email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.drop()

    
