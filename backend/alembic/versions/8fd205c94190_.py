"""empty message

Revision ID: 8fd205c94190
Revises:
Create Date: 2019-01-26 14:06:54.785820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fd205c94190'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('testtable',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(50)))
    pass


def downgrade():
    op.drop_table('testtable')
