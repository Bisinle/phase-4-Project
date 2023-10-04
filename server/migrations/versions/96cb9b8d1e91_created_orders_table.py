"""created orders table 

Revision ID: 96cb9b8d1e91
Revises: 0b281600a33f
Create Date: 2023-10-04 14:28:57.502844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96cb9b8d1e91'
down_revision = '0b281600a33f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_price', sa.Integer(), nullable=True),
    sa.Column('item_quantity', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###