"""timestamp

Revision ID: 184ed7dba4a6
Revises: c1fbec22b33f
Create Date: 2020-09-13 19:13:19.853950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '184ed7dba4a6'
down_revision = 'c1fbec22b33f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxes', sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('taxes', 'timestamp')
    # ### end Alembic commands ###