"""change pessoa id_pessoa from integer to uuid

Revision ID: 20250101_uuid_pessoa
Revises: 20251125_categoria
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '20250101_uuid_pessoa'
down_revision = '20251125_categoria'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alterar coluna id_pessoa na tabela pessoa de INTEGER para UUID
    # Primeiro, remover a constraint de primary key
    op.drop_constraint('pessoa_pkey', 'pessoa', type_='primary')
    
    # Remover a constraint de foreign key das tabelas relacionadas temporariamente
    op.drop_constraint('sessao_fk_pessoa_id_pessoa_fkey', 'sessao', type_='foreignkey')
    op.drop_constraint('meta_fk_pessoa_id_pessoa_fkey', 'meta', type_='foreignkey')
    op.drop_constraint('alerta_fk_pessoa_id_pessoa_fkey', 'alerta', type_='foreignkey')
    op.drop_constraint('assinatura_fk_pessoa_id_pessoa_fkey', 'assinatura', type_='foreignkey')
    
    # Criar uma coluna temporária UUID
    op.add_column('pessoa', sa.Column('id_pessoa_new', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Gerar UUIDs para registros existentes (se houver)
    op.execute("UPDATE pessoa SET id_pessoa_new = gen_random_uuid()")
    
    # Alterar as foreign keys relacionadas para UUID também
    op.add_column('sessao', sa.Column('fk_pessoa_id_pessoa_new', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('meta', sa.Column('fk_pessoa_id_pessoa_new', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('alerta', sa.Column('fk_pessoa_id_pessoa_new', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('assinatura', sa.Column('fk_pessoa_id_pessoa_new', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Copiar os UUIDs correspondentes para as foreign keys
    op.execute("""
        UPDATE sessao s
        SET fk_pessoa_id_pessoa_new = p.id_pessoa_new
        FROM pessoa p
        WHERE s.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    op.execute("""
        UPDATE meta m
        SET fk_pessoa_id_pessoa_new = p.id_pessoa_new
        FROM pessoa p
        WHERE m.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    op.execute("""
        UPDATE alerta a
        SET fk_pessoa_id_pessoa_new = p.id_pessoa_new
        FROM pessoa p
        WHERE a.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    op.execute("""
        UPDATE assinatura a
        SET fk_pessoa_id_pessoa_new = p.id_pessoa_new
        FROM pessoa p
        WHERE a.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    # Remover as colunas antigas
    op.drop_column('sessao', 'fk_pessoa_id_pessoa')
    op.drop_column('meta', 'fk_pessoa_id_pessoa')
    op.drop_column('alerta', 'fk_pessoa_id_pessoa')
    op.drop_column('assinatura', 'fk_pessoa_id_pessoa')
    op.drop_column('pessoa', 'id_pessoa')
    
    # Renomear as colunas novas
    op.rename_column('pessoa', 'id_pessoa_new', 'id_pessoa')
    op.rename_column('sessao', 'fk_pessoa_id_pessoa_new', 'fk_pessoa_id_pessoa')
    op.rename_column('meta', 'fk_pessoa_id_pessoa_new', 'fk_pessoa_id_pessoa')
    op.rename_column('alerta', 'fk_pessoa_id_pessoa_new', 'fk_pessoa_id_pessoa')
    op.rename_column('assinatura', 'fk_pessoa_id_pessoa_new', 'fk_pessoa_id_pessoa')
    
    # Tornar as colunas NOT NULL
    op.alter_column('pessoa', 'id_pessoa', nullable=False)
    op.alter_column('sessao', 'fk_pessoa_id_pessoa', nullable=False)
    op.alter_column('meta', 'fk_pessoa_id_pessoa', nullable=False)
    op.alter_column('alerta', 'fk_pessoa_id_pessoa', nullable=False)
    op.alter_column('assinatura', 'fk_pessoa_id_pessoa', nullable=False)
    
    # Adicionar primary key constraint na nova coluna UUID
    op.create_primary_key('pessoa_pkey', 'pessoa', ['id_pessoa'])
    
    # Recriar as foreign keys
    op.create_foreign_key(
        'sessao_fk_pessoa_id_pessoa_fkey',
        'sessao', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'meta_fk_pessoa_id_pessoa_fkey',
        'meta', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'alerta_fk_pessoa_id_pessoa_fkey',
        'alerta', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'assinatura_fk_pessoa_id_pessoa_fkey',
        'assinatura', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # Reverter para INTEGER (nota: isso pode perder dados se houver UUIDs que não podem ser convertidos)
    # Esta operação é complexa e pode não ser totalmente reversível
    # Em produção, considere fazer backup antes de fazer downgrade
    
    # Remover foreign keys
    op.drop_constraint('sessao_fk_pessoa_id_pessoa_fkey', 'sessao', type_='foreignkey')
    op.drop_constraint('meta_fk_pessoa_id_pessoa_fkey', 'meta', type_='foreignkey')
    op.drop_constraint('alerta_fk_pessoa_id_pessoa_fkey', 'alerta', type_='foreignkey')
    op.drop_constraint('assinatura_fk_pessoa_id_pessoa_fkey', 'assinatura', type_='foreignkey')
    
    # Remover primary key
    op.drop_constraint('pessoa_pkey', 'pessoa', type_='primary')
    
    # Adicionar colunas INTEGER temporárias
    op.add_column('pessoa', sa.Column('id_pessoa_old', sa.Integer(), nullable=True, autoincrement=True))
    op.add_column('sessao', sa.Column('fk_pessoa_id_pessoa_old', sa.Integer(), nullable=True))
    op.add_column('meta', sa.Column('fk_pessoa_id_pessoa_old', sa.Integer(), nullable=True))
    op.add_column('alerta', sa.Column('fk_pessoa_id_pessoa_old', sa.Integer(), nullable=True))
    op.add_column('assinatura', sa.Column('fk_pessoa_id_pessoa_old', sa.Integer(), nullable=True))
    
    # Gerar IDs sequenciais (não há como recuperar os IDs originais)
    op.execute("""
        WITH numbered AS (
            SELECT id_pessoa, ROW_NUMBER() OVER (ORDER BY id_pessoa) as rn
            FROM pessoa
        )
        UPDATE pessoa SET id_pessoa_old = numbered.rn
        FROM numbered
        WHERE pessoa.id_pessoa = numbered.id_pessoa
    """)
    
    # Atualizar foreign keys
    op.execute("""
        UPDATE sessao s
        SET fk_pessoa_id_pessoa_old = p.id_pessoa_old
        FROM pessoa p
        WHERE s.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    op.execute("""
        UPDATE meta m
        SET fk_pessoa_id_pessoa_old = p.id_pessoa_old
        FROM pessoa p
        WHERE m.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    op.execute("""
        UPDATE alerta a
        SET fk_pessoa_id_pessoa_old = p.id_pessoa_old
        FROM pessoa p
        WHERE a.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    op.execute("""
        UPDATE assinatura a
        SET fk_pessoa_id_pessoa_old = p.id_pessoa_old
        FROM pessoa p
        WHERE a.fk_pessoa_id_pessoa = p.id_pessoa
    """)
    
    # Remover colunas UUID
    op.drop_column('sessao', 'fk_pessoa_id_pessoa')
    op.drop_column('meta', 'fk_pessoa_id_pessoa')
    op.drop_column('alerta', 'fk_pessoa_id_pessoa')
    op.drop_column('assinatura', 'fk_pessoa_id_pessoa')
    op.drop_column('pessoa', 'id_pessoa')
    
    # Renomear colunas antigas
    op.rename_column('pessoa', 'id_pessoa_old', 'id_pessoa')
    op.rename_column('sessao', 'fk_pessoa_id_pessoa_old', 'fk_pessoa_id_pessoa')
    op.rename_column('meta', 'fk_pessoa_id_pessoa_old', 'fk_pessoa_id_pessoa')
    op.rename_column('alerta', 'fk_pessoa_id_pessoa_old', 'fk_pessoa_id_pessoa')
    op.rename_column('assinatura', 'fk_pessoa_id_pessoa_old', 'fk_pessoa_id_pessoa')
    
    # Tornar NOT NULL
    op.alter_column('pessoa', 'id_pessoa', nullable=False)
    op.alter_column('sessao', 'fk_pessoa_id_pessoa', nullable=False)
    op.alter_column('meta', 'fk_pessoa_id_pessoa', nullable=False)
    op.alter_column('alerta', 'fk_pessoa_id_pessoa', nullable=False)
    op.alter_column('assinatura', 'fk_pessoa_id_pessoa', nullable=False)
    
    # Recriar primary key e foreign keys
    op.create_primary_key('pessoa_pkey', 'pessoa', ['id_pessoa'])
    op.create_foreign_key(
        'sessao_fk_pessoa_id_pessoa_fkey',
        'sessao', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'meta_fk_pessoa_id_pessoa_fkey',
        'meta', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'alerta_fk_pessoa_id_pessoa_fkey',
        'alerta', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'assinatura_fk_pessoa_id_pessoa_fkey',
        'assinatura', 'pessoa',
        ['fk_pessoa_id_pessoa'], ['id_pessoa'],
        ondelete='CASCADE'
    )

