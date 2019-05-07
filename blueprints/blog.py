from flask import Blueprint

from blog.extensions import db
from blog.models import Post, Category

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """
    homepage for unauthorized visitors
    :return: json object: (article list, category list)
    """
    # articles = db.session.query(Post).order_by(Post.created_at).desc().all()
    # categories = db.session.query(Category).order_by(Category.name).desc().all()
    return 'blog'
