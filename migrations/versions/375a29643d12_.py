"""empty message

Revision ID: 375a29643d12
Revises: 34963f38651b
Create Date: 2023-11-21 16:59:38.466262

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '375a29643d12'
down_revision = '34963f38651b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_processos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prioridade_demanda', sa.String(length=50), nullable=True))
        batch_op.drop_column('status_demanda')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_processos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_demanda', mysql.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('prioridade_demanda')

    # ### end Alembic commands ###
