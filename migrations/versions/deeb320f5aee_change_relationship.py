"""change relationship

Revision ID: deeb320f5aee
Revises: 062fa88b9638
Create Date: 2022-04-03 13:21:57.990380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deeb320f5aee'
down_revision = '062fa88b9638'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('comments', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('review', 'comments')
    # ### end Alembic commands ###
