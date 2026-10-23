from datetime import date
from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_RN_008_duplicata_segunda_recusada(colaborador, periodo_julho, calcular_lote_fn):
    base = dict(
        data=date(2026, 7, 9),
        categoria_raw="alimentacao",
        descricao="Almoco",
        fornecedor="Bistro Central",
        valor=Decimal("54.90"),
    )
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(id="d-006", **base),
                despesa(id="d-007", **base),
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("54.90")
    assert resultado.itens[1].valor_reembolsavel == Decimal("0")
