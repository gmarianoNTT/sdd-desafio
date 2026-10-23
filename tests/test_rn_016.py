from datetime import date
from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_RN_016_AMB_020_limite_500_nao_pendente(colaborador, periodo_julho, calcular_lote_fn):
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="h-1",
                    data=date(2026, 7, 14),
                    categoria_raw="hospedagem",
                    descricao="Hotel - 2 diarias",
                    valor=Decimal("500"),
                    tem_nota_fiscal=True,
                )
            ],
        )
    )
    item = resultado.itens[0]
    assert item.valor_reembolsavel == Decimal("500.00")
    assert item.status == "aprovado"


def test_RN_016_pendente_reembolso_maior_que_500(colaborador, periodo_julho, calcular_lote_fn):
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="h-2",
                    data=date(2026, 7, 14),
                    categoria_raw="hospedagem",
                    descricao="Hotel - 2 diarias",
                    valor=Decimal("800"),
                    tem_nota_fiscal=True,
                )
            ],
        )
    )
    item = resultado.itens[0]
    assert item.valor_reembolsavel == Decimal("750.00")
    assert item.status == "pendente"
