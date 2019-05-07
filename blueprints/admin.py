from flask import (flash, json, jsonify, request)
from flask import Blueprint

from blog.extensions import db
from blog.models import Post

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/', methods=['GET'])
def index():
    return 'hello from admin page'


@admin_bp.route('/articles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def article_crud():
    if request.method == 'GET':
        return get_articles()

    args = request.get_json()

    if request.method == 'PUT':
        id_, title, body = args.get('id', ''), args.get('title', ''), args.get('body', '')
        return update_article(id_, title, body)

    if request.method == 'POST':
        id_, title, body = args.get('id', ''), args.get('title', ''), args.get('body', '')
        return create_article(title, body)

    if request.method == 'DELETE':
        id_ = args.get('id', '')
        return delete_article(id_)


def create_article(title, body):
    created = Post.create(title=title, body=body)
    if created:
        return jsonify({'state': '201 Created'})
    return jsonify({'state': '409 Conflict'})


def update_article(id_, title, body):
    if all([id_]) and any([title, body]):
        updated = Post.update(id_=id_, title=title, body=body)
        if not updated:
            return jsonify({'state': '404 Not Found'})
        return jsonify({'state': '200 OK'})


def delete_article(id_):
    deleted = Post.delete(id_)
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
