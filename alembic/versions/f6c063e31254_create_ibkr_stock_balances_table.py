"""create_ibkr_stock_balances_table

Revision ID: f6c063e31254
Revises: 33a24868dd4a
Create Date: 2025-10-04 21:46:08.139024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6c063e31254'
down_revision: Union[str, None] = '33a24868dd4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ibkr_stock_balances',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=15, scale=4), nullable=False),
        sa.Column('average_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('current_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['ibkr_users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_ibkr_stock_balances_user_id', 'ibkr_stock_balances', ['user_id'])
    op.create_index('idx_ibkr_stock_balances_user_ticker', 'ibkr_stock_balances', ['user_id', 'ticker'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_ibkr_stock_balances_user_ticker', table_name='ibkr_stock_balances')
    op.drop_index('idx_ibkr_stock_balances_user_id', table_name='ibkr_stock_balances')
    op.drop_table('ibkr_stock_balances')
