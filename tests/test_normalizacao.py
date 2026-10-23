from datetime import date
from decimal import Decimal

from reembolso.motor.normalizacao import normalizar_categoria
from tests.conftest import despesa, lote_de_despesas


def test_AMB_010_categoria_maiuscula(colaborador, periodo_julho, calcular_lote_fn):
    assert normalizar_categoria("ALIMENTACAO") == "alimentacao"
    resultado = calcular_lote_fn(
        lote_de_despesas(
            colaborador,
            periodo_julho,
            [
                despesa(
                    id="d-014",
                    data=date(2026, 7, 31),
                    categoria_raw="ALIMENTACAO",
                    valor=Decimal("61"),
                )
            ],
        )
    )
    item = resultado.itens[0]
    assert item.valor_reembolsavel == Decimal("60.00")
    assert item.status == "parcial"
