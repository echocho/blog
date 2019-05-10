from flask import (jsonify, request, Blueprint)
from flask_login import current_user, login_required

from blog.extensions import db
from blog.models import Admin, Post
from utils import (create_article, update_article, delete_article, get_articles,
                   get_category_lst, create_category, delete_category)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/', methods=['GET'])
def index():
    return 'hello from admin page'


@admin_bp.route('/articles/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def article_crud():
    if request.method == 'GET':
        return get_articles()

    args = request.get_json()
    id, title, body, category_name = args.get('id', ''), args.get('title', ''), \
                                      args.get('body', ''), args.get('category', '')

    if request.method == 'PUT':
        return update_article(id, title, body, category_name)

    if request.method == 'POST':
        return create_article(title, body, category_name)

    if request.method == 'DELETE':
        return delete_article(id)


@admin_bp.route('/category/', methods=['GET', 'POST', 'DELETE'])
@login_required
def category_crud():
    if request.method == 'GET':
        categories =  get_category_lst()
        return jsonify({'state': '200 OK',
                         'data': categories})

    name = request.get_json().get('name', '')

    if request.method == 'POST':
        return create_category(name)

    if request.method == 'DELETE':
        return delete_category(name)


@admin_bp.route('/profile/', methods=['GET', 'PUT'])
@login_required
def edit_profile():
    if request.method == 'PUT':
        args = request.get_json()
        blog_name, about, blog_subtitle = args.get('blog_name', None), args.get('about', None), args.get('blog_subtitle', None)
        blog = db.session.query(Admin).filter_by(username=current_user.username).first()
        if blog_name:
            blog.blog_name = blog_name
        if about:
            blog.about = about
        if blog_subtitle:
            blog.blog_subtitle = blog_subtitle
        db.session.commit()
        return jsonify({'state': '200 OK'})
    return jsonify({'data': {'username': current_user.username,
                             'email': current_user.email,
                             'blog_name': current_user.blog_name,
                             'about': current_user.about,
                             'blog_subtitle': current_user.blog_subtitle}})