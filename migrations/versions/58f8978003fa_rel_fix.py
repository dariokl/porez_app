"""rel fix

Revision ID: 58f8978003fa
Revises: 
Create Date: 2020-10-18 13:35:37.637679

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '58f8978003fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('taxes', 'user_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('taxes', 'user_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
