from flask import (jsonify, request, Blueprint)
from flask_login import login_required

from blog.extensions import db
from blog.models import Post

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


def create_article(title, body, category_name):
    created = Post.create(title=title, body=body, category_name=category_name)
    if created:
        return jsonify({'state': '201 Created'})
    return jsonify({'state': '409 Conflict'})


def update_article(id, title, body, category_name):
    if all([id]) and any([title, body]):
        updated = Post.update(id=id, title=title, body=body, category_name=category_name)
        if not updated:
            return jsonify({'state': '404 Not Found'})
        return jsonify({'state': '200 OK'})


def delete_article(id):
    deleted = Post.delete(id)
    if deleted:
        return jsonify({'state': '200 OK'})
    return jsonify({'state': '404 Not Found'})


def get_articles():
    posts = db.session.query(Post).all()
    if posts:
        title_lst = [post.title for post in posts]
        body_lst = [post.body for post in posts]
        return_elements = ['title', 'body']
        articles = list(dict(zip(return_elements, title_body)) for title_body in list(zip(title_lst, body_lst)))

        return jsonify({'state': '200 OK',
                        'articles': articles})

    return jsonify({'state': '200 OK',
                    'articles': []})
