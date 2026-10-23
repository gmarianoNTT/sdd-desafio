from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from reembolso.motor.models import Colaborador, Despesa, Lote, Periodo


@pytest.fixture
def periodo_julho() -> Periodo:
    return Periodo(
        competencia="2026-07",
        inicio=date(2026, 7, 1),
        fim=date(2026, 7, 31),
    )


@pytest.fixture
def colaborador() -> Colaborador:
    return Colaborador(id="c-1", nome="Teste", centro_custo="CC-1")


def despesa(**kwargs) -> Despesa:
    defaults = {
        "id": "d-x",
        "data": date(2026, 7, 3),
        "categoria_raw": "alimentacao",
        "descricao": "Almoco",
        "fornecedor": "Bar",
        "valor": Decimal("50"),
        "tem_nota_fiscal": True,
    }
    defaults.update(kwargs)
    return Despesa(**defaults)


def lote_de_despesas(colaborador: Colaborador, periodo: Periodo, despesas: list[Despesa]) -> Lote:
    return Lote(colaborador=colaborador, periodo=periodo, despesas=despesas)
