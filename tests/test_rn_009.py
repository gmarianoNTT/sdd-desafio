from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_RN_009_coworking_recusado(colaborador, periodo_julho, calcular_lote_fn):
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [despesa(id="d-005", categoria_raw="coworking", valor=Decimal("89"))],
        )
    )
    item = resultado.itens[0]
    assert item.valor_reembolsavel == Decimal("0")
    assert item.status == "recusado"
