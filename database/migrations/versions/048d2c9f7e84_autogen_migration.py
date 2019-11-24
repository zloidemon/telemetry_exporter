"""Autogen migration

Revision ID: 048d2c9f7e84
Revises: 
Create Date: 2019-11-22 14:59:47.894963

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '048d2c9f7e84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telemetry',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('delivered', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('metric', sa.Integer(), nullable=False),
    sa.Column('key', sa.Integer(), nullable=False),
    sa.Column('value', sa.BigInteger(), nullable=False),
    sa.Column('labels', postgresql.ARRAY(sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_telemetry_created'), 'telemetry', ['created'], unique=False)
    op.create_index(op.f('ix_telemetry_key'), 'telemetry', ['key'], unique=False)
    op.create_index(op.f('ix_telemetry_metric'), 'telemetry', ['metric'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_telemetry_metric'), table_name='telemetry')
    op.drop_index(op.f('ix_telemetry_key'), table_name='telemetry')
    op.drop_index(op.f('ix_telemetry_created'), table_name='telemetry')
    op.drop_table('telemetry')
    # ### end Alembic commands ###
