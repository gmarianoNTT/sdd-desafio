from decimal import Decimal
from pathlib import Path

from reembolso.io.json_io import ler_lote
from reembolso.motor.calcular import calcular_lote


def _item(resultado, id_despesa: str):
    return next(i for i in resultado.itens if i.id == id_despesa)


def test_exemplo_completo_ids_criticos():
    raiz = Path(__file__).resolve().parents[1]
    lote = ler_lote(raiz / "exemplos" / "despesas-exemplo.json")
    resultado = calcular_lote(lote)

    assert _item(resultado, "d-001").valor_reembolsavel == Decimal("60.00")
    assert _item(resultado, "d-001").status == "parcial"
    assert _item(resultado, "d-002").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-003").valor_reembolsavel == Decimal("80.00")
    assert _item(resultado, "d-004").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-005").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-006").valor_reembolsavel == Decimal("54.90")
    assert _item(resultado, "d-007").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-008").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-009").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-010").valor_reembolsavel == Decimal("480.00")
    assert _item(resultado, "d-011").valor_reembolsavel == Decimal("33.33")
    assert _item(resultado, "d-012").valor_reembolsavel == Decimal("47.20")
    assert _item(resultado, "d-013").valor_reembolsavel == Decimal("0")
    assert _item(resultado, "d-014").valor_reembolsavel == Decimal("60.00")

    assert resultado.total_reembolsavel == sum(
        i.valor_reembolsavel for i in resultado.itens
    )
