from datetime import date
from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_RN_013_conversao_eur(periodo_julho, calcular_lote_fn):
    from reembolso.motor.models import Colaborador

    colaborador = Colaborador(id="c-x", nome="X", centro_custo="CC-COMERCIAL")
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="eur-1",
                    data=date(2026, 7, 14),
                    valor=Decimal("22"),
                    moeda="EUR",
                )
            ],
        )
    )
    item = resultado.itens[0]
    assert item.valor_informado == Decimal("22.00")
    assert item.valor_reembolsavel == Decimal("90.00")
    assert item.status == "parcial"
