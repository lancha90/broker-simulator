"""create_ibkr_users_table

Revision ID: 33a24868dd4a
Revises: 55c37baaa218
Create Date: 2025-10-04 21:45:41.278988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33a24868dd4a'
down_revision: Union[str, None] = '55c37baaa218'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ibkr_users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('api_key', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ibkr_users_api_key', 'ibkr_users', ['api_key'], unique=True)
    op.create_index('idx_ibkr_users_email', 'ibkr_users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_ibkr_users_email', table_name='ibkr_users')
    op.drop_index('idx_ibkr_users_api_key', table_name='ibkr_users')
    op.drop_table('ibkr_users')
