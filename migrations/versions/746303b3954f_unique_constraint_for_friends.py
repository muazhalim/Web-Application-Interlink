"""Unique constraint for Friends

Revision ID: 746303b3954f
Revises: c80648474058
Create Date: 2023-12-05 00:13:40.546792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '746303b3954f'
down_revision = 'c80648474058'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('friends', schema=None) as batch_op:
        batch_op.create_unique_constraint('_user_friend_uc', ['user_id', 'friend_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('friends', schema=None) as batch_op:
        batch_op.create_unique_constraint('_user_friend_uc', ['user_id', 'friend_id'])


    # ### end Alembic commands ###
