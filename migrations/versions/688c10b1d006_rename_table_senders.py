"""rename table senders

Revision ID: 688c10b1d006
Revises: 5858e5570fe7
Create Date: 2020-05-29 15:13:05.150737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '688c10b1d006'
down_revision = '5858e5570fe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('senders',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('message_id', sa.BigInteger(), nullable=True),
    sa.Column('channel_id', sa.BigInteger(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('message_channels')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_channels',
    sa.Column('message_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('channel_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('status_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], name='message_channels_channel_id_fkey'),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name='message_channels_message_id_fkey'),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], name='message_channels_status_id_fkey'),
    sa.PrimaryKeyConstraint('message_id', 'channel_id', name='message_channels_pkey')
    )
    op.drop_table('senders')
    # ### end Alembic commands ###