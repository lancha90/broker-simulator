"""create_ibkr_trades_table

Revision ID: fe94ecebcec0
Revises: f6c063e31254
Create Date: 2025-10-04 21:46:35.247951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe94ecebcec0'
down_revision: Union[str, None] = 'f6c063e31254'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ibkr_trades',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('trade_type', sa.String(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=15, scale=4), nullable=False),
        sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['ibkr_users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_ibkr_trades_user_id', 'ibkr_trades', ['user_id'])
    op.create_index('idx_ibkr_trades_created_at', 'ibkr_trades', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_ibkr_trades_created_at', table_name='ibkr_trades')
    op.drop_index('idx_ibkr_trades_user_id', table_name='ibkr_trades')
    op.drop_table('ibkr_trades')
