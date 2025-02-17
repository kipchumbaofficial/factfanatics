"""Removed total questions

Revision ID: 4567788bb92d
Revises: f212699c5acc
Create Date: 2025-01-09 15:40:58.240915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4567788bb92d'
down_revision = 'f212699c5acc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_answers', schema=None) as batch_op:
        batch_op.drop_column('total_questions')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_questions', mysql.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
