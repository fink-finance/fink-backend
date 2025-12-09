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
    # Verifica se a coluna existe antes de tentar renomear usando SQL direto
    conn = op.get_bind()
    
    # Verifica se descricao existe
    result = conn.execute(sa.text("""
        SELECT COUNT(*) 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'meta' 
        AND column_name = 'descricao'
    """))
    descricao_count = result.scalar() if hasattr(result, 'scalar') else list(result)[0][0]
    
    # Verifica se categoria existe
    result = conn.execute(sa.text("""
        SELECT COUNT(*) 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'meta' 
        AND column_name = 'categoria'
    """))
    categoria_count = result.scalar() if hasattr(result, 'scalar') else list(result)[0][0]
    
    if descricao_count > 0 and categoria_count == 0:
        # Renomeia descricao para categoria
        op.alter_column('meta', 'descricao', new_column_name='categoria')
    elif categoria_count > 0:
        # Coluna já foi renomeada ou sempre existiu como categoria - não faz nada
        pass
    else:
        # Se nenhuma das colunas existe, cria categoria (não deveria acontecer)
        op.add_column('meta', sa.Column('categoria', sa.String(length=500), nullable=False, server_default='Outros'))


def downgrade() -> None:
    # Rename column back from categoria to descricao
    op.alter_column('meta', 'categoria', new_column_name='descricao')
