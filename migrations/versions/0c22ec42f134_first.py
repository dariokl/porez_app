"""first

Revision ID: 0c22ec42f134
Revises: 
Create Date: 2020-07-27 19:53:33.274797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c22ec42f134'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ime', sa.String(length=64), nullable=True),
    sa.Column('prezime', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('jmbg', sa.Integer(), nullable=True),
    sa.Column('kontakt_tel', sa.Integer(), nullable=True),
    sa.Column('grad', sa.String(), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('expire', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###