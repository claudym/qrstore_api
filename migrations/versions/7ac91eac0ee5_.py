"""empty message

Revision ID: 7ac91eac0ee5
Revises: 6218fd805d75
Create Date: 2022-09-14 08:04:04.400266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ac91eac0ee5'
down_revision = '6218fd805d75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('hashed', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=70), nullable=True),
    sa.Column('last_name', sa.String(length=70), nullable=True),
    sa.Column('tax_id', sa.String(length=50), nullable=True),
    sa.Column('photo', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
