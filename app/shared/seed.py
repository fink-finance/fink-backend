# app/shared/seed.py
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import async_session_maker  # ajusta o nome se for diferente

from app.identidade.persistence.pessoa_orm import PessoaORM
from app.identidade.persistence.sessao_orm import SessaoORM  # se não usar, pode remover
from app.metas.persistence.meta_orm import MetaORM
from app.alertas.persistence.alerta_orm import AlertaORM
from app.comercial.persistence.plano_orm import PlanoORM
from app.comercial.persistence.assinatura_orm import AssinaturaORM
from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM
from app.comercial.persistence.solicitacao_pagamento_orm import SolicitacaoPagamentoORM


DEMO_EMAIL = "demo@fink.dev"


async def seed_db() -> None:
    print("[SEED] Iniciando seed do banco...")
    async with async_session_maker() as session:
        await seed_tipos_pagamento(session)
        await seed_planos(session)
        pessoa_demo = await seed_pessoa_demo(session)
        meta_demos = await seed_metas_demo(session, pessoa_demo)
        assinatura_demo = await seed_assinatura_demo(session, pessoa_demo)
        await seed_solicitacao_pagamento_demo(session, assinatura_demo)
        await seed_alertas_demo(session, pessoa_demo, meta_demos)
    print("[SEED] Seed finalizado com sucesso!")



# --------------------- TIPOS DE PAGAMENTO ---------------------


async def seed_tipos_pagamento(session: AsyncSession) -> None:
    """
    Cria alguns tipos de pagamento padrão se ainda não existirem.
    """
    # Se já existir pelo menos um, não faz nada
    result = await session.execute(select(TipoPagamentoORM).limit(1))
    exists = result.scalar_one_or_none()
    if exists:
        return

    tipos = [
        "Cartão de Crédito",
        "Cartão de Débito",
        "Pix",
        "Boleto",
    ]

    session.add_all([TipoPagamentoORM(tipo_pagamento=nome) for nome in tipos])
    await session.commit()


# -------------------------- PLANOS ----------------------------


async def seed_planos(session: AsyncSession) -> None:
    """
    Cria alguns planos comerciais padrão se ainda não existirem.
    """
    result = await session.execute(select(PlanoORM).limit(1))
    exists = result.scalar_one_or_none()
    if exists:
        return

    planos = [
        PlanoORM(
            titulo="Gratuito",
            descricao="Plano básico para começar a organizar as finanças.",
            preco=0.0,
            duracao_meses=0,
            status="ativo",
        ),
        PlanoORM(
            titulo="Essencial",
            descricao="Plano com recursos principais para acompanhamento mensal.",
            preco=19.90,
            duracao_meses=1,
            status="ativo",
        ),
        PlanoORM(
            titulo="Premium",
            descricao="Plano completo com relatórios avançados e integrações extras.",
            preco=39.90,
            duracao_meses=1,
            status="ativo",
        ),
    ]

    session.add_all(planos)
    await session.commit()


# -------------------------- PESSOA ----------------------------


async def seed_pessoa_demo(session: AsyncSession) -> PessoaORM:
    """
    Cria uma pessoa demo para testes.
    """
    result = await session.execute(
        select(PessoaORM).where(PessoaORM.email == DEMO_EMAIL)
    )
    pessoa = result.scalar_one_or_none()
    if pessoa:
        return pessoa

    pessoa = PessoaORM(
        email=DEMO_EMAIL,
        senha="demo123",  # em produção deveria ser hash!
        nome="Usuário Demo",
        data_nascimento=date(2000, 1, 1),
        telefone="81999999999",
        genero="nao_informado",
        estado="PE",
        cidade="Recife",
        rua="Rua de Exemplo",
        numero="123",
        cep="50000000",
        admin=False,
    )

    session.add(pessoa)
    await session.commit()
    await session.refresh(pessoa)
    return pessoa


# --------------------------- META -----------------------------


async def seed_metas_demo(session: AsyncSession, pessoa: PessoaORM) -> list[MetaORM]:
    """
    Cria várias metas financeiras demo para a pessoa demo.
    Retorna a lista de metas da pessoa (as já existentes + as criadas aqui).
    """
    metas_config = [
        {
            "titulo": "Reserva de Emergência",
            "descricao": "Construir uma reserva equivalente a 6 meses de despesas.",
            "valor_alvo": Decimal("5000.00"),
            "valor_atual": Decimal("500.00"),
            # termina no fim do próximo ano
            "termina_em": date(date.today().year + 1, 12, 31),
        },
        {
            "titulo": "Quitar Cartão de Crédito",
            "descricao": "Zerar o saldo devedor do cartão de crédito principal.",
            "valor_alvo": Decimal("3000.00"),
            "valor_atual": Decimal("1200.00"),
            # daqui a 6 meses (aproximado em dias)
            "termina_em": date.fromordinal(date.today().toordinal() + 180),
        },
        {
            "titulo": "Viagem de Férias",
            "descricao": "Juntar dinheiro para uma viagem de férias no fim do ano.",
            "valor_alvo": Decimal("8000.00"),
            "valor_atual": Decimal("2000.00"),
            "termina_em": date(date.today().year + 1, 1, 31),
        },
    ]

    metas_criadas: list[MetaORM] = []

    for cfg in metas_config:
        # Verifica se essa meta já existe para a pessoa
        result = await session.execute(
            select(MetaORM).where(
                MetaORM.fk_pessoa_id_pessoa == pessoa.id_pessoa,
                MetaORM.titulo == cfg["titulo"],
            )
        )
        meta = result.scalar_one_or_none()
        if meta is None:
            meta = MetaORM(
                fk_pessoa_id_pessoa=pessoa.id_pessoa,
                titulo=cfg["titulo"],
                descricao=cfg["descricao"],
                valor_alvo=cfg["valor_alvo"],
                valor_atual=cfg["valor_atual"],
                criada_em=date.today(),  # ✅ Define a data atual
                termina_em=cfg["termina_em"],
                status="em_andamento",  # ✅ Define o status inicial
            )
            session.add(meta)
            await session.commit()
            await session.refresh(meta)
        metas_criadas.append(meta)

    return metas_criadas

# ------------------------ ASSINATURA --------------------------


async def seed_assinatura_demo(session: AsyncSession, pessoa: PessoaORM) -> AssinaturaORM:
    """
    Cria uma assinatura demo para a pessoa demo, usando o plano 'Essencial'
    (ou o primeiro plano disponível).
    """
    # Verificar se a pessoa já tem alguma assinatura
    result = await session.execute(
        select(AssinaturaORM).where(AssinaturaORM.fk_pessoa_id_pessoa == pessoa.id_pessoa)
    )
    assinatura = result.scalar_one_or_none()
    if assinatura:
        return assinatura

    # Buscar um plano para vincular
    result_plano = await session.execute(
        select(PlanoORM).where(PlanoORM.titulo == "Essencial")
    )
    plano = result_plano.scalar_one_or_none()
    if not plano:
        # fallback: pega qualquer plano
        result_plano = await session.execute(select(PlanoORM).limit(1))
        plano = result_plano.scalar_one()

    hoje = date.today()
    termina = date(hoje.year, hoje.month, hoje.day)
    # se duracao_meses > 0, você pode sofisticar isso depois
    # por enquanto deixamos com termina_em = hoje + 30 dias:
    termina = date.fromordinal(hoje.toordinal() + 30)

    assinatura = AssinaturaORM(
        fk_pessoa_id_pessoa=pessoa.id_pessoa,
        fk_plano_id_plano=plano.id_plano,
        comeca_em=hoje,
        termina_em=termina,
        status="ativa",
    )

    session.add(assinatura)
    await session.commit()
    await session.refresh(assinatura)
    return assinatura


# ------------------- SOLICITAÇÃO PAGAMENTO -------------------


async def seed_solicitacao_pagamento_demo(
    session: AsyncSession,
    assinatura: AssinaturaORM,
) -> None:
    """
    Cria uma solicitação de pagamento demo para a assinatura demo.
    """
    result = await session.execute(
        select(SolicitacaoPagamentoORM).where(
            SolicitacaoPagamentoORM.fk_assinatura_id_assinatura == assinatura.id_assinatura
        )
    )
    existe = result.scalar_one_or_none()
    if existe:
        return

    # Escolher um tipo de pagamento (ex.: 'Pix')
    result_tipo = await session.execute(
        select(TipoPagamentoORM).where(TipoPagamentoORM.tipo_pagamento == "Pix")
    )
    tipo = result_tipo.scalar_one_or_none()
    if not tipo:
        # fallback: pega qualquer tipo
        result_tipo = await session.execute(select(TipoPagamentoORM).limit(1))
        tipo = result_tipo.scalar_one()

    solicitacao = SolicitacaoPagamentoORM(
        fk_tipo_pagamento_id_pagamento=tipo.id_pagamento,
        fk_assinatura_id_assinatura=assinatura.id_assinatura,
        data_hora=datetime.utcnow(),
    )

    session.add(solicitacao)
    await session.commit()


# --------------------------- ALERTA ---------------------------


async def seed_alertas_demo(
    session: AsyncSession,
    pessoa: PessoaORM,
    metas: list[MetaORM],
) -> None:
    """
    Cria múltiplos alertas para a pessoa demo e suas metas.

    Exemplos de alertas:
    - progresso_meta >= 80% (para todas as metas)
    - progresso_meta >= 100% (meta concluída)
    - dias_para_termino <= 7 (alerta de prazo curto)
    """
    for meta in metas:
        # 1) Alerta de meta quase concluída (80%)
        await _ensure_alert(
            session=session,
            pessoa_id=pessoa.id_pessoa,
            meta_id=meta.id_meta,
            parametro="progresso_meta",
            acao="maior_ou_igual_que",
            valor=80.0,
        )

        # 2) Alerta de meta concluída (100%)
        await _ensure_alert(
            session=session,
            pessoa_id=pessoa.id_pessoa,
            meta_id=meta.id_meta,
            parametro="progresso_meta",
            acao="maior_ou_igual_que",
            valor=100.0,
        )

        # 3) Alerta de prazo curto (7 dias para terminar)
        await _ensure_alert(
            session=session,
            pessoa_id=pessoa.id_pessoa,
            meta_id=meta.id_meta,
            parametro="dias_para_termino",
            acao="menor_ou_igual_que",
            valor=7.0,
        )

    # Exemplo de alerta global (sem meta específica): saldo geral muito baixo
    await _ensure_alert(
        session=session,
        pessoa_id=pessoa.id_pessoa,
        meta_id=None,
        parametro="saldo_geral",
        acao="menor_ou_igual_que",
        valor=100.0,
    )


async def _ensure_alert(
    session: AsyncSession,
    pessoa_id: int,
    meta_id: int | None,
    parametro: str,
    acao: str,
    valor: float,
) -> None:
    """
    Garante que exista um alerta com os parâmetros dados.
    Se já existir, não cria outro (idempotente).
    """
    query = select(AlertaORM).where(
        AlertaORM.fk_pessoa_id_pessoa == pessoa_id,
        AlertaORM.parametro == parametro,
        AlertaORM.acao == acao,
        AlertaORM.valor == valor,
    )
    if meta_id is not None:
        query = query.where(AlertaORM.fk_meta_id_meta == meta_id)
    else:
        query = query.where(AlertaORM.fk_meta_id_meta.is_(None))  # type: ignore[arg-type]

    result = await session.execute(query)
    exists = result.scalar_one_or_none()
    if exists:
        return

    alerta = AlertaORM(
        fk_pessoa_id_pessoa=pessoa_id,
        fk_meta_id_meta=meta_id,
        parametro=parametro,
        acao=acao,
        valor=valor,
    )
    session.add(alerta)
    await session.commit()
