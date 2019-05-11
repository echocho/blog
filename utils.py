from flask import jsonify

from blog.extensions import db
from blog.models import Category, Comment, Post

DEFAULT_BODY_SUMMARY_LENGTH = 150


def get_article_lst():
    """
    :return: id, title, first 150 characters of body
    :rtype: list()
    """
    articles = Post.get_all()
    article_lst = list(dict(zip(('id', 'title', 'body'),
                                (article.id, article.title, article.body[:DEFAULT_BODY_SUMMARY_LENGTH])))
                       for article in articles)
    return article_lst


def get_category_lst():
    """
    :return: id, name
    :rtype: list()
    """
    categories = Category.get()
    category_lst = list(dict(zip(('id', 'name'), (category.id, category.name))) for category in categories)
    return category_lst


def get_comment_lst():
    """
    :return: id, author, email, body, post_id, replied_id, replies_ids
    :rtype: list()
    """
    comments = Comment.get_all()
    comment_lst = list(dict(zip(('id', 'name', 'email', 'post_id', 'body', 'replied_id'),
                                (comment.id, comment.author, comment.email,
                                comment.post_id, comment.body, comment.replied_id))) for comment in comments)
    return comment_lst


def create_category(name):
    created = Category.create(name)
    if created:
        return jsonify({'state': '201 Created'})
    return jsonify({'state': '409 Conflict'})


def delete_category(name):
    deleted = Category.delete(name)
    if deleted:
        return jsonify({'state': '200 OK'})
    return jsonify({'state': '404 Not Found'})


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