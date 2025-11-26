"""rename descricao to categoria in meta table

Revision ID: 20251125_categoria
Revises: 20251122_defaults
Create Date: 2025-11-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251125_categoria'
down_revision = '20251122_defaults'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename column descricao to categoria in meta table
    op.alter_column('meta', 'descricao', new_column_name='categoria')


def downgrade() -> None:
    # Rename column back from categoria to descricao
    op.alter_column('meta', 'categoria', new_column_name='descricao')
