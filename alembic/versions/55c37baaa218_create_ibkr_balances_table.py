"""create_ibkr_balances_table

Revision ID: 55c37baaa218
Revises: 
Create Date: 2025-10-04 21:36:15.182084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55c37baaa218'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ibkr_balances',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('cash_balance', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ibkr_balances_user_id', 'ibkr_balances', ['user_id'])


def downgrade() -> None:
    op.drop_index('idx_ibkr_balances_user_id', table_name='ibkr_balances')
    op.drop_table('ibkr_balances')