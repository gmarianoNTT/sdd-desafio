from datetime import date
from decimal import Decimal

from reembolso.motor.calcular import calcular_lote
from tests.conftest import despesa, lote_de_despesas


def test_RN_006_alimentacao_90_em_viagem(colaborador, periodo_julho):
    resultado = calcular_lote(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-010",
                    data=date(2026, 7, 14),
                    categoria_raw="hospedagem",
                    descricao="Hotel Rio - 2 diarias",
                    valor=Decimal("480"),
                ),
                despesa(
                    id="d-011",
                    data=date(2026, 7, 15),
                    categoria_raw="alimentacao",
                    valor=Decimal("33.333"),
                ),
            ],
        )
    )
    alimentacao = resultado.itens[1]
    assert alimentacao.valor_reembolsavel == Decimal("33.33")
    assert alimentacao.status == "aprovado"
