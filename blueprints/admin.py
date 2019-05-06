from flask import Blueprint
from flask import flash, request
from models import Post

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def index():
    pass


@admin_bp.route('/articles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def article_crud():
    if request.method == 'GET':
        get_articles()
    elif request.args:
        _id, title, body = request.args.get('id'), request.args.get('title'), request.args.get('body')
        if request.method == 'POST' and all([_id]) and any([title, body]):
            update_article(_id, title, body)
            # TODO: should respond something in json
            return flash('Article Updated')

        if request.method == 'PUT' and all([_id, title, body]):
            create_article(id, title, body)
            # TODO: should respond something in json
            return flash('Article Craeted')

        if request.method == 'DELETE':
            delete_article(_id)
            #TODO: should respond something in json
            return flash('Article Delete')


def create_article(_id, title, body):
    Post.create(id=_id, title=title, body=body)


def update_article(_id, title, body):
    Post.update(id=_id, title=title, body=body)


def delete_article(_id):
    Post.delete(_id)


def get_articles():
    pass
