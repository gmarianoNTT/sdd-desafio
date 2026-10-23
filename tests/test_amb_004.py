from datetime import date

from reembolso.motor.viagem import datas_em_viagem
from tests.conftest import despesa


def test_AMB_004_datas_viagem_de_hospedagem():
    despesas = [
        despesa(
            id="d-010",
            data=date(2026, 7, 14),
            categoria_raw="hospedagem",
            descricao="Hotel Rio - 2 diarias",
        ),
        despesa(
            id="d-013",
            data=date(2026, 7, 22),
            categoria_raw="hospedagem",
            descricao="Airbnb 3 noites",
        ),
    ]
    datas = datas_em_viagem(despesas)
    assert date(2026, 7, 14) in datas
    assert date(2026, 7, 15) in datas
    assert date(2026, 7, 22) in datas
    assert date(2026, 7, 24) in datas
    assert date(2026, 7, 18) not in datas
