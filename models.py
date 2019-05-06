from datetime import datetime

from extensions import db

print(db)
print(dir(db))
print('Model' in dir(db))

class Admin(db.Model):
    __tablename__ = 'blog_admin'
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    blog_name = db.Column(db.String(150))
    blog_sub_title = db.Column(db.String(250))
    about = db.Column(db.String(450))
    # TODO: relationship with post


class Post(db.Model):
    __tablename__ = 'blog_post'
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String)
    created_at = db.Column(default=datetime.utcnow())
    # TODO: relationship with category

    @staticmethod
    def create(id_, title, body):
        if all([id_, title, body]):
            new_post = Post(id_, title, body)
            db.session.add(new_post)
            db.comit()

    @staticmethod
    def delete(id_):
        db.session.filter_by(id_=id_).delete()
        db.commit()

    @staticmethod
    def update(id_, title=None, body=None):
        post = db.session.filter_by(id_=id_).first()
        if title:
            post.title = title
        if body:
            post.body = body
        post.session.commit()


class Category(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    @staticmethod
    def delete(id_):
        db.session.filter_by(id_=id_).delete()
        db.commit()

    @staticmethod
    def create(name):
        if name and (not db.session.filter_by(name=name).first()):
            category = Category(name=name)
            db.session.add(category)
            db.commit()

    @staticmethod
    def get():
        categories = db.session.all()
        return categories


# class Comment(db.Model):
#     id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     body = db.Column(db.String)
#     replied_to = ??

