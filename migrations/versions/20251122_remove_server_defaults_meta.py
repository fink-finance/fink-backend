"""remove server defaults from meta

Revision ID: 20251122_defaults
Revises: 085059e62f7a
Create Date: 2025-11-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251122_defaults'
down_revision = '085059e62f7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remove server defaults from meta table
    op.alter_column('meta', 'valor_atual',
                    existing_type=sa.NUMERIC(precision=10, scale=2),
                    server_default=None,
                    existing_nullable=False)
    
    op.alter_column('meta', 'criada_em',
                    existing_type=sa.DATE(),
                    server_default=None,
                    existing_nullable=False)
    
    op.alter_column('meta', 'status',
                    existing_type=sa.VARCHAR(length=20),
                    server_default=None,
                    existing_nullable=False)


def downgrade() -> None:
    # Restore server defaults
    op.alter_column('meta', 'status',
                    existing_type=sa.VARCHAR(length=20),
                    server_default="em_andamento",
                    existing_nullable=False)
    
    op.alter_column('meta', 'criada_em',
                    existing_type=sa.DATE(),
                    server_default=sa.text('CURRENT_DATE'),
                    existing_nullable=False)
    
    op.alter_column('meta', 'valor_atual',
                    existing_type=sa.NUMERIC(precision=10, scale=2),
                    server_default="0",
                    existing_nullable=False)
