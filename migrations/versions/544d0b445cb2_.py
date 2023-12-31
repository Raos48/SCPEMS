"""empty message

Revision ID: 544d0b445cb2
Revises: 3af9fbf23d5f
Create Date: 2023-12-16 18:23:03.855764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '544d0b445cb2'
down_revision = '3af9fbf23d5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_processos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo_determinacao', sa.String(length=60), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_processos', schema=None) as batch_op:
        batch_op.drop_column('tipo_determinacao')

    # ### end Alembic commands ###
