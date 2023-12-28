"""empty message

Revision ID: 3cc7fd903c3e
Revises: 9755a9f0dcb9
Create Date: 2023-12-05 21:21:21.563743

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3cc7fd903c3e'
down_revision = '9755a9f0dcb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_designados', schema=None) as batch_op:
        batch_op.drop_column('servico_servidor')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_designados', schema=None) as batch_op:
        batch_op.add_column(sa.Column('servico_servidor', mysql.VARCHAR(length=100), nullable=False))

    # ### end Alembic commands ###
