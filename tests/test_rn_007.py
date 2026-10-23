from datetime import date
from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_RN_007_fora_competencia(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-008",
                    data=date(2026, 4, 15),
                    valor=Decimal("41"),
                )
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("0")
