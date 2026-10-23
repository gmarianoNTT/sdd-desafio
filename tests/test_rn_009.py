from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_RN_009_coworking_recusado(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [despesa(id="d-005", categoria_raw="coworking", valor=Decimal("89"))],
        )
    )
    item = resultado.itens[0]
    assert item.valor_reembolsavel == Decimal("0")
    assert item.status == "recusado"
