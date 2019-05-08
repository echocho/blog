from flask import Blueprint, jsonify

from blog.models import Post, Category, Comment

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """
    homepage for unauthorized visitors
    :return: json object: article list, category list
    """
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

