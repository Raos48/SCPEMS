"""empty message

Revision ID: 7445e85c2ed5
Revises: bf7692eefdfa
Create Date: 2023-11-28 18:48:35.862688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7445e85c2ed5'
down_revision = 'bf7692eefdfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_designados', schema=None) as batch_op:
        batch_op.add_column(sa.Column('servico_servidor', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_designados', schema=None) as batch_op:
        batch_op.drop_column('servico_servidor')

    # ### end Alembic commands ###
