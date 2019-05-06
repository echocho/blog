from extensions import db

print(db)
print(dir(db))
print('Model' in dir(db))

class Admin(db.Model):
    __tablename__ = 'blog_admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    blog_name = db.Column(db.String(150))
    blog_sub_title = db.Column(db.String(250))
    about = db.Column(db.String(450))
    # TODO: relationship with post


class Post(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String)
    # TODO: relationship with category

    @staticmethod
    def create(id, title, body):
        if all([id, title, body]):
            new_post = Post(id, title, body)
            db.session.add(new_post)
            db.comit()

    @staticmethod
    def delete(id):
        db.session.filter_by(id=id).delete()
        db.commit()

    @staticmethod
    def update(id, title=None, body=None):
        post = db.session.filter_by(id=id).first()
        if title:
            post.title = title
        if body:
            post.body = body
        post.session.commit()

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     body = db.Column(db.String)
#     replied_to = ??
#
# class Category(db.Model):
#     pass