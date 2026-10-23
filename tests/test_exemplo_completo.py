from decimal import Decimal
from pathlib import Path

from reembolso.io.json_io import ler_lote


def _item(resultado, id_despesa: str):
    return next(i for i in resultado.itens if i.id == id_despesa)


def test_exemplo_completo_ids_criticos(calcular_lote_fn):
    raiz = Path(__file__).resolve().parents[1]
    lote = ler_lote(raiz / "exemplos" / "despesas-exemplo.json")
    resultado = calcular_lote_fn(lote)

    assert _item(resultado, "d-001").valor_reembolsavel == Decimal("72.50")
    assert _item(resultado, "d-001").status == "aprovado"
    assert _item(resultado, "d-002").valor_reembolsavel == Decimal("2.50")
    assert _item(resultado, "d-002").status == "parcial"
    assert _item(resultado, "d-003").valor_reembolsavel == Decimal("80.00")
    assert _item(resultado, "d-004").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-005").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-006").valor_reembolsavel == Decimal("54.90")
    assert _item(resultado, "d-007").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-008").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-009").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-010").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-011").valor_reembolsavel == Decimal("33.33")
    assert _item(resultado, "d-012").valor_reembolsavel == Decimal("47.20")
    assert _item(resultado, "d-013").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-014").valor_reembolsavel == Decimal("61.00")
    assert _item(resultado, "d-014").status == "aprovado"

    assert resultado.total_reembolsavel == sum(
        i.valor_reembolsavel for i in resultado.itens
    )
