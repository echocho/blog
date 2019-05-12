from flask import url_for
import unittest

from blog import create_app
from blog.extensions import db
from blog.models import Admin, Category, Comment, Post
from tests.base import BaseTestCase


class TestBlog(BaseTestCase):
    def setUp(self):
        super(TestBlog, self).setUp()

        category = Category(name='category 1')
        post = Post(id=1, title='title 1', body='body 1', category=category)
        comment = Comment(author='author 1', email='a@email.com', body='comment 1', post=post)

        db.session.add_all([category, comment, post])
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.drop()

    def test_index(self):
        response = self.client.get('/')
        data = response.get_data.json()
        self.assertEqual(data == {"articles": [
                                        {
                                          "body": "body 1",
                                          "id": 1,
                                          "title": "title 1"
                                        }
                                      ],
                                      "categories": [
                                        {
                                          "id": 1,
                                          "name": "category 1"
                                        }
                                      ],
                                      "comments": [
                                        {
                                          "body": "comment 1",
                                          "email": "a@email.com",
                                          "id": 1,
                                          "name": "author 1",
                                          "post_id": 1,
                                          "replied_id": None
                                        }
                                      ]
                                    })


