from extensions import db

print(db)
print(dir(db))
print('Model' in dir(db))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    blog_name = db.Column(db.String(150))
    blog_sub_title = db.Column(db.String(250))
    about = db.Column(db.String(450))

