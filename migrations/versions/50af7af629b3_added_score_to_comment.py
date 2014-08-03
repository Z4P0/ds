"""added score to comment

Revision ID: 50af7af629b3
Revises: 3b3cbf41ce05
Create Date: 2014-08-03 02:08:29.252901

"""

# revision identifiers, used by Alembic.
revision = '50af7af629b3'
down_revision = '3b3cbf41ce05'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('score', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'score')
    ### end Alembic commands ###