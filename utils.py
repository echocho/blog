from blog.models import Category, Comment, Post

DEFAULT_BODY_SUMMARY_LENGTH = 150


def get_article_lst():
    """
    :return: id, title, first 150 characters of body
    :rtype: list()
    """
    articles = Post.get()
    article_lst = list(dict(zip(('id', 'title', 'body'), \
                                (article.id, article.title, article.body[:DEFAULT_BODY_SUMMARY_LENGTH]))) \
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
    comments = Comment.get()
    comment_lst = list(dict(zip(('id', 'name', 'email', 'post_id', 'body', 'replied_id'),
                                (comment.id, comment.author, comment.email,
                                comment.post_id, comment.body, comment.replied_id))) for comment in comments)
    return comment_lst
