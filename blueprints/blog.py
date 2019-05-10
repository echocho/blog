from flask import Blueprint, jsonify, make_response, request

from blog.extensions import db
from blog.models import Admin, Category, Comment, Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """
    homepage for unauthorized visitors
    :return: json object: article list, category list
    """
    # raise Exception(request.cookies)
    articles = Post.get()
    categories = Category.get()
    comments = Comment.get()
    article_lst = list(dict(zip(('id', 'title', 'body'), \
                                (article.id, article.title, article.body))) \
                                for article in articles)
    category_lst = list(dict(zip(('id', 'name'), (category.id, category.name))) for category in categories)
    comment_lst = list(dict(zip(('id', 'name'), (comment.id, comment.author, comment.email, comment.post_id, \
                                              comment.replied_id))) for comment in comments)
    return jsonify({'articles': article_lst,
                    'categories': category_lst,
                    'comments': comment_lst})

# from flask import make_response
# @blog_bp.route('/cookie/')
# def cookie():
#     res = make_response('setting a cookie')
#     res.set_cookie('foo', 'bar', max_age=670*60*21*2)
#     return res
#
#
# @blog_bp.route('/remove-cookie/')
# def delete_cookie():
#     res = make_response('deleting cookie')
#     res.set_cookie('foo', 'bar', max_age=0)
#     return res
#


@blog_bp.route('/register/', methods=['GET', 'POST'])
def register():
    args = request.get_json()
    username, password, email = args.get('username'), args.get('password'), args.get('email')
    if all([username, password, email]):
        exists = db.session.query(Admin).filter_by(email=email, username=username).first()
        if exists:
            return jsonify({'state': '409 Conflict'})
        hashed = Admin().hash_password(password)
        user = Admin(username=username, password_hash=hashed, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({'state': '201 Created'})

