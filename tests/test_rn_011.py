from datetime import date
from decimal import Decimal

from reembolso.motor.monetario import arredondar_moeda
from tests.conftest import despesa, lote_de_despesas


def test_RN_011_arredondamento_d011(colaborador, periodo_julho, calcular_lote_fn):
    assert arredondar_moeda(Decimal("33.333")) == Decimal("33.33")
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-010",
                    data=date(2026, 7, 14),
                    categoria_raw="hospedagem",
                    descricao="Hotel - 2 diarias",
                    valor=Decimal("480"),
                ),
                despesa(
                    id="d-011",
                    data=date(2026, 7, 15),
                    valor=Decimal("33.333"),
                ),
            ],
        )
    )
    assert resultado.itens[1].valor_reembolsavel == Decimal("33.33")
