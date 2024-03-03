"""empty message

Revision ID: ed43efee8a62
Revises: 68cd40f494f2
Create Date: 2024-02-18 18:24:44.918279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed43efee8a62'
down_revision = '68cd40f494f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_competencias', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_atribuicoes', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_competencias', schema=None) as batch_op:
        batch_op.drop_column('total_atribuicoes')

    # ### end Alembic commands ###