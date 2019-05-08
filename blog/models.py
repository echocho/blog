from datetime import datetime

from .extensions import db


class Admin(db.Model):
    __tablename__ = 'blog_admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    blog_name = db.Column(db.String(150))
    blog_sub_title = db.Column(db.String(250))
    about = db.Column(db.String(450))


class Category(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    posts = db.relationship('Post', back_populates='category')

    @staticmethod
    def delete(id):
        db.session.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def create(name):
        if name and (not db.session.query(Category).filter_by(name=name).first()):
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            return db.session.query(Category).filter_by(name=name).first()

    @staticmethod
    def get():
        categories = db.session.all()
        return categories


class Post(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


    @staticmethod
    def create(title, body, category_name):
        exists = db.session.query(Post).filter_by(title=title, body=body).first()
        if not exists:
            # check if category exists, if not, create one and link post with category
            category = create_category_if_not_exists(category_name)
            new_post = Post(title=title, body=body, category=category)
            db.session.add(new_post)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete(id):
        try:
            db.session.query(Post).filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            pass
        return False

    @staticmethod
    def update(id, title=None, body=None, category_name=None):
        post = db.session.query(Post).filter_by(id=id).first()
        if not post:
            return False
        if title:
            post.title = title
        if body:
            post.body = body
        if category_name:
            category = create_category_if_not_exists(category_name)
            post.category = category
        db.session.commit()
        return True


def create_category_if_not_exists(category_name):
    """
    if a category exists, return this category object;
    otherwise, create a new category
    :param category_name:
    :return: category object
    """
    category = db.session.query(Category).filter_by(name=category_name).first()
    if not category:
        category = Category.create(category_name)
    return category


class Comment(db.Model):
    __tablename__ = 'blog_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    body = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    post = db.relationship('Post', back_populates='comments')
    replied_id = db.Column(db.Integer, db.ForeignKey('blog_comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')



