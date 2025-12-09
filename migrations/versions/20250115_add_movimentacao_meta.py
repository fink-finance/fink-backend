"""add movimentacao_meta table

Revision ID: 20250115_movimentacao_meta
Revises: 20250101_uuid_pessoa
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250115_movimentacao_meta'
down_revision = '20250101_uuid_pessoa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria tabela movimentacao_meta para registro de movimentações de metas."""
    op.create_table(
        'movimentacao_meta',
        sa.Column('id_movimentacao', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('fk_meta_id_meta', sa.Integer(), nullable=False),
        sa.Column('valor', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('acao', sa.String(length=20), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id_movimentacao'),
        sa.CheckConstraint("acao IN ('adicionado', 'retirado')", name='movimentacao_meta_acao_check'),
        sa.ForeignKeyConstraint(['fk_meta_id_meta'], ['meta.id_meta'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    """Remove tabela movimentacao_meta."""
    op.drop_table('movimentacao_meta')

