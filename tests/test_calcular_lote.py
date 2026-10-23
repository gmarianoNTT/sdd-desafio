from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_calcular_lote_retorna_mesmos_ids(colaborador, periodo_julho, calcular_lote_fn):
    despesas = [
        despesa(id="a"),
        despesa(id="b", valor=Decimal("10")),
    ]
    resultado = calcular_lote_fn(lote_de_despesas(colaborador, periodo_julho, despesas))
    assert [i.id for i in resultado.itens] == ["a", "b"]
