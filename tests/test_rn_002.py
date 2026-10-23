from datetime import date
from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_RN_002_limite_transporte_80(colaborador, periodo_julho):
    dia = date(2026, 7, 10)
    despesas = [
        despesa(
            id=f"t{i}",
            data=dia,
            categoria_raw="transporte_urbano",
            descricao=f"Corrida {i}",
            valor=Decimal("30"),
            tem_nota_fiscal=False,
        )
        for i in range(3)
    ]
    resultado = calcular_lote(lote_de_despesas(colaborador, periodo_julho, despesas))
    assert resultado.itens[0].valor_reembolsavel == Decimal("30.00")
    assert resultado.itens[1].valor_reembolsavel == Decimal("30.00")
    assert resultado.itens[2].valor_reembolsavel == Decimal("20.00")
    assert resultado.itens[2].status == "parcial"
