from datetime import date
from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_RN_005_nf_100_exato_ok(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-003",
                    data=date(2026, 7, 6),
                    categoria_raw="transporte_urbano",
                    valor=Decimal("100"),
                    tem_nota_fiscal=False,
                )
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("80.00")
    assert resultado.itens[0].status == "parcial"


def test_RN_005_nf_100_01_recusa(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-004",
                    data=date(2026, 7, 6),
                    categoria_raw="transporte_urbano",
                    valor=Decimal("100.01"),
                    tem_nota_fiscal=False,
                )
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("0")
