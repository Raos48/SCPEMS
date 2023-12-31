"""empty message

Revision ID: 9a7d2d3e70d7
Revises: 22ab2757143c
Create Date: 2023-11-11 23:32:53.511057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9a7d2d3e70d7'
down_revision = '22ab2757143c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_processos', schema=None) as batch_op:
        batch_op.alter_column('tipo_determinacao',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_processos', schema=None) as batch_op:
        batch_op.alter_column('tipo_determinacao',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=True)

    # ### end Alembic commands ###
