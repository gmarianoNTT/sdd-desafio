from datetime import date
from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_RN_001_d001_d002_limite_60(colaborador, periodo_julho, calcular_lote_fn):
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-001",
                    data=date(2026, 7, 3),
                    valor=Decimal("72.50"),
                ),
                despesa(
                    id="d-002",
                    data=date(2026, 7, 3),
                    valor=Decimal("38.00"),
                ),
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("60.00")
    assert resultado.itens[0].status == "parcial"
    assert resultado.itens[1].valor_reembolsavel == Decimal("0")
    assert resultado.itens[1].status == "recusado"
