"""add groups to animals

Revision ID: 77cb1a7ef6ce
Revises: 5fa013e56d60
Create Date: 2021-10-05 20:36:22.062585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77cb1a7ef6ce'
down_revision = '5fa013e56d60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('predators', sa.Column('group', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('predators', 'group')
    # ### end Alembic commands ###
