"""empty message

Revision ID: 02da9e34c3e9
Revises: ad3dd8db24b9
Create Date: 2023-12-10 12:49:02.868796

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '02da9e34c3e9'
down_revision = 'ad3dd8db24b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_requests', schema=None) as batch_op:
        pass

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_requests', schema=None) as batch_op:
        pass


    # ### end Alembic commands ###
