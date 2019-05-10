from flask import Blueprint, jsonify, redirect, request, url_for
from flask_login import login_required

from blog.extensions import db
from blog.models import Admin, Comment
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
        author, email, body, replied_id = args.get('author', ''), args.get('email', ''), \
                                          args.get('body', ''), args.get('replied_id', '')
        if all([author, email, body]):
            comment = Comment(author=author, email=email, body=body, post_id=post_id)
            if type(replied_id) is int:
                comment.replied_id = replied_id
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('blog.post_details', id=post_id)) #TODO: redirect but stays on the same page


@blog_bp.route('/article/<int:id>/', methods=['GET'])
def post_details(id):
    return jsonify({'state': 'you are reading article {}'.format(id)})
