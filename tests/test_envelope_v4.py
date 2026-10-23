from decimal import Decimal
from pathlib import Path

from reembolso.io.json_io import ler_lote


def _item(resultado, id_despesa: str):
    return next(i for i in resultado.itens if i.id == id_despesa)


def test_envelope_cc_comercial(calcular_lote_fn):
    raiz = Path(__file__).resolve().parents[1]
    lote = ler_lote(raiz / "exemplos" / "envelope" / "despesas-envelope.json")
    resultado = calcular_lote_fn(lote)

    assert _item(resultado, "e-001").valor_reembolsavel == Decimal("300.00")
    assert _item(resultado, "e-001").status == "parcial"
    assert _item(resultado, "e-005").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "e-006").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "e-009").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "e-007").valor_reembolsavel == Decimal("1200.00")
    assert _item(resultado, "e-007").status == "pendente"


def test_envelope_cc_desconhecido(calcular_lote_fn):
    raiz = Path(__file__).resolve().parents[1]
    lote = ler_lote(
        raiz / "exemplos" / "envelope" / "despesas-envelope-cc-desconhecido.json"
    )
    resultado = calcular_lote_fn(lote)

    assert _item(resultado, "f-001").valor_reembolsavel == Decimal("58.00")
    assert _item(resultado, "f-002").valor_reembolsavel == Decimal("310.00")
    assert _item(resultado, "f-002").status == "aprovado"
    assert _item(resultado, "f-003").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "f-004").valor_reembolsavel == Decimal("65.76")
