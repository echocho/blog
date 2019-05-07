from datetime import datetime

from .extensions import db


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    # TODO: relationship with category

    @staticmethod
    def create(title, body):
        exists = db.session.query(Post).filter_by(title=title, body=body).first()
        if not exists:
            new_post = Post(title=title, body=body)
            db.session.add(new_post)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete(id_):
        try:
            db.session.query(Post).filter_by(id_=int(id_)).delete()
            db.session.commit()
            return True
        except:
            pass
        return False

    @staticmethod
    def update(id_, title=None, body=None):
        post = db.session.query(Post).filter_by(id_=int(id_)).first()
        if not post:
            return False
        if title:
            post.title = title
        if body:
            post.body = body
        db.session.commit()
        return True


class Category(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    @staticmethod
    def delete(id_):
        db.session.filter_by(id_=id_).delete()
        db.session.commit()

    @staticmethod
    def create(name):
        if name and (not db.session.filter_by(name=name).first()):
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()

    @staticmethod
    def get():
        categories = db.session.all()
        return categories


# class Comment(db.Model):
#     id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     body = db.Column(db.String)
#     replied_to = ??

