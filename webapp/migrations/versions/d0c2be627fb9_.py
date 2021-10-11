"""empty message

Revision ID: d0c2be627fb9
Revises: 869e02fbf42b
Create Date: 2021-10-10 20:03:23.254914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0c2be627fb9'
down_revision = '869e02fbf42b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flatprice_input', sa.Column('OUTPUT', sa.Integer(), nullable=True))
    op.add_column('resale_input', sa.Column('OUTPUT', sa.Integer(), nullable=True))
    op.add_column('town_input', sa.Column('OUTPUT', sa.Integer(), nullable=True))
    op.drop_column('town_input', 'town')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('town_input', sa.Column('town', sa.VARCHAR(length=64), nullable=True))
    op.drop_column('town_input', 'OUTPUT')
    op.drop_column('resale_input', 'OUTPUT')
    op.drop_column('flatprice_input', 'OUTPUT')
    # ### end Alembic commands ###