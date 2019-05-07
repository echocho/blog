from flask import (flash, jsonify, request)
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
        get_articles()
    elif request.args:
        id_, title, body = request.args.get('id'), request.args.get('title'), request.args.get('body')
        if request.method == 'POST' and all([id_]) and any([title, body]):
            update_article(id_, title, body)
            # TODO: should respond something in json
            return flash('Article Updated')

        if request.method == 'PUT' and all([id_, title, body]):
            create_article(id, title, body)
            # TODO: should respond something in json
            return flash('Article Created')

        if request.method == 'DELETE':
            delete_article(id_)
            # TODO: should respond something in json
            return flash('Article Delete')


def create_article(id_, title, body):
    Post.create(id_=id_, title=title, body=body)


def update_article(id_, title, body):
    Post.update(id_=id_, title=title, body=body)


def delete_article(id_):
    Post.delete(id_)


def get_articles():
    posts = db.session.query(Post).all()
    if posts:
        title_lst = [post.title for post in posts]
        body_lst = [post.body for post in posts]
        return_elements = ['title', 'body']
        articles = list(dict(zip(return_elements, title_body)) for title_body in list(zip(title_lst, body_lst)))

        return jsonify({'state': 201,
                        'articles': articles})
