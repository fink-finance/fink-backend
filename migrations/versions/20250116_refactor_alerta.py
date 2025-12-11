"""refactor alerta table structure

Revision ID: 20250116_refactor_alerta
Revises: 20250115_movimentacao_meta
Create Date: 2025-01-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '20250116_refactor_alerta'
down_revision = '20250115_movimentacao_meta'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Refatora tabela alerta: remove campos antigos e adiciona novos campos."""
    
    # Remover foreign key constraint para meta (se existir)
    op.drop_constraint('alerta_fk_meta_id_meta_fkey', 'alerta', type_='foreignkey', if_exists=True)
    
    # Remover colunas antigas
    op.drop_column('alerta', 'fk_meta_id_meta', if_exists=True)
    op.drop_column('alerta', 'parametro', if_exists=True)
    op.drop_column('alerta', 'acao', if_exists=True)
    op.drop_column('alerta', 'valor', if_exists=True)
    
    # Adicionar novas colunas
    op.add_column('alerta', sa.Column('data', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('alerta', sa.Column('conteudo', sa.String(), nullable=False, server_default=''))
    op.add_column('alerta', sa.Column('lida', sa.Boolean(), nullable=False, server_default='false'))
    
    # Remover server defaults após adicionar as colunas (para permitir valores NULL em criações futuras)
    op.alter_column('alerta', 'data', server_default=None)
    op.alter_column('alerta', 'conteudo', server_default=None)
    op.alter_column('alerta', 'lida', server_default=None)


def downgrade() -> None:
    """Reverte mudanças na tabela alerta."""
    
    # Remover novas colunas
    op.drop_column('alerta', 'lida', if_exists=True)
    op.drop_column('alerta', 'conteudo', if_exists=True)
    op.drop_column('alerta', 'data', if_exists=True)
    
    # Restaurar colunas antigas
    op.add_column('alerta', sa.Column('valor', sa.Float(), nullable=True))
    op.add_column('alerta', sa.Column('acao', sa.String(), nullable=True))
    op.add_column('alerta', sa.Column('parametro', sa.String(), nullable=True))
    op.add_column('alerta', sa.Column('fk_meta_id_meta', sa.Integer(), nullable=True))
    
    # Restaurar foreign key constraint para meta
    op.create_foreign_key(
        'alerta_fk_meta_id_meta_fkey',
        'alerta', 'meta',
        ['fk_meta_id_meta'], ['id_meta'],
        ondelete='SET NULL'
    )

