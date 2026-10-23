from datetime import date
from decimal import Decimal

from tests.conftest import despesa, lote_de_despesas


def test_RN_003_hospedagem_d010_rateio(colaborador, periodo_julho, calcular_lote_fn):
    resultado = calcular_lote_fn(
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
                    tem_nota_fiscal=True,
                )
            ],
        )
    )
    assert resultado.itens[0].valor_reembolsavel == Decimal("480.00")
    assert resultado.itens[0].status == "aprovado"
