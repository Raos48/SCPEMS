"""empty message

Revision ID: 9755a9f0dcb9
Revises: d6bac09a5fb5
Create Date: 2023-12-05 17:53:29.261577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9755a9f0dcb9'
down_revision = 'd6bac09a5fb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_designados', schema=None) as batch_op:
        batch_op.alter_column('afastamento_servidor',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.String(length=3),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_designados', schema=None) as batch_op:
        batch_op.alter_column('afastamento_servidor',
               existing_type=sa.String(length=3),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)

    # ### end Alembic commands ###
