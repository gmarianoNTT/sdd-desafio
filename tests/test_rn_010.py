from datetime import date
from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_RN_010_estorno_zero_e_devolve_saldo(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-009",
                    data=date(2026, 7, 11),
                    categoria_raw="transporte_urbano",
                    valor=Decimal("-45"),
                    tem_nota_fiscal=False,
                ),
                despesa(
                    id="pos",
                    data=date(2026, 7, 11),
                    categoria_raw="transporte_urbano",
                    valor=Decimal("80"),
                    tem_nota_fiscal=False,
                ),
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("0")
    assert resultado.itens[1].valor_reembolsavel == Decimal("80.00")
