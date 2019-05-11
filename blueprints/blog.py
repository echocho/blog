from flask import Blueprint, jsonify, redirect, request, url_for
from flask_login import login_required

from blog.extensions import db
from blog.models import Admin, Category, Comment, Post
from utils import get_article_lst, get_category_lst, get_comment_lst

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """
    homepage for unauthorized visitors
    :return: json object: article list, category list, comment list
    """
    articles = get_article_lst()
    categories = get_category_lst()
    comments = get_comment_lst()
    return jsonify({'articles': articles,
                    'categories': categories,
                    'comments': comments})


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


@blog_bp.route('/check/', methods=['GET'])
@login_required
def authenticated():
    return jsonify({'state': '200 OK',
                    'desc': 'you are authenticated!'})


@blog_bp.route('/article/<int:post_id>/comments/', methods=['POST'])
def comment(post_id):
    if request.method == 'POST':
        args = request.get_json()
        author, email, body, replied_id = args.get('author', None), args.get('email', None), \
                                          args.get('body', None), args.get('replied_id', None)
        if all([author, email, body]):
            comment = Comment(author=author, email=email, body=body, post_id=post_id)
            if type(replied_id) is int:
                comment.replied_id = replied_id
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('blog.post_details', id=post_id)) #TODO: redirect but stays on the same page


@blog_bp.route('/article/<int:id>/', methods=['GET'])
def post_details(id):
    """
    :param id:
    :return: id, title, full body, category, comments[replied_id]
    """
    post = Post.get(id)
    if not post:
        return jsonify({'state': '404 Not Found'})
    category = db.session.query(Category.name).filter_by(id=post.category_id).first()
    comments = db.session.query(Comment).filter_by(post_id=id).all()
    if comments:
        comments = list(dict(zip(('id', 'author', 'email', 'body', 'replied_id'),
                                 (c.id, c.author, c.email, c.body, c.replied_id))) for c in comments)
    return jsonify({'state': '200 OK',
                    'data': {'post_id': id,
                             'category': category,
                             'comments': comments}})

