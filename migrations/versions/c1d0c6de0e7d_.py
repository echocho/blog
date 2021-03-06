"""empty message

Revision ID: c1d0c6de0e7d
Revises: 5477c35a2a1c
Create Date: 2019-05-08 21:21:52.260197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d0c6de0e7d'
down_revision = '5477c35a2a1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['blog_post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_comment')
    # ### end Alembic commands ###
