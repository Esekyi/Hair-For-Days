"""deleted name column

Revision ID: 4b8e7861a078
Revises: 1d69659cc512
Create Date: 2021-11-29 07:57:35.075285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b8e7861a078'
down_revision = '1d69659cc512'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('register', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('register', sa.Column('name', sa.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###
