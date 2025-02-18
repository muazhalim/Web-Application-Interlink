"""added hashed_password

Revision ID: 37b0513e402c
Revises: a56c5bf40a05
Create Date: 2023-11-26 15:23:00.103341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b0513e402c'
down_revision = 'a56c5bf40a05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_password', sa.String(length=128), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('hashed_password')

    # ### end Alembic commands ###
