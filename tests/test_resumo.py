from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_resumo_soma_itens(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(id="a", valor=Decimal("10")),
                despesa(id="b", valor=Decimal("20")),
            ],
        )
    )
    soma_informado = sum(i.valor_informado for i in resultado.itens)
    soma_reembolsavel = sum(i.valor_reembolsavel for i in resultado.itens)
    assert resultado.total_informado == soma_informado
    assert resultado.total_reembolsavel == soma_reembolsavel
