"""empty message

Revision ID: 00c98d51f66b
Revises: a84ef9ca02d3
Create Date: 2023-11-07 19:11:09.940529

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '00c98d51f66b'
down_revision = 'a84ef9ca02d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_usuarios', schema=None) as batch_op:
        batch_op.alter_column('usuario',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_usuarios', schema=None) as batch_op:
        batch_op.alter_column('usuario',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###
