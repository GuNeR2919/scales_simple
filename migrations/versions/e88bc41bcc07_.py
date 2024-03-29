"""empty message

Revision ID: e88bc41bcc07
Revises: 
Create Date: 2023-12-28 13:09:12.265945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e88bc41bcc07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weight',
    sa.Column('rowid', sa.Integer(), nullable=False),
    sa.Column('mtime', sa.Integer(), nullable=True),
    sa.Column('yard', sa.String(length=8), nullable=True),
    sa.Column('rbook', sa.Integer(), nullable=True),
    sa.Column('typ', sa.String(length=1), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('pid', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('rowid')
    )
    with op.batch_alter_table('weight', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_weight_mtime'), ['mtime'], unique=True)
        batch_op.create_index(batch_op.f('ix_weight_yard'), ['yard'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weight', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_weight_yard'))
        batch_op.drop_index(batch_op.f('ix_weight_mtime'))

    op.drop_table('weight')
    # ### end Alembic commands ###
