"""typo

Revision ID: 5fa013e56d60
Revises: 326db3740ff0
Create Date: 2021-08-31 19:07:15.034481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa013e56d60'
down_revision = '326db3740ff0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('predators', sa.Column('classification', sa.String(length=255), nullable=True))
    op.drop_column('predators', 'classicication')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('predators', sa.Column('classicication', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('predators', 'classification')
    # ### end Alembic commands ###
