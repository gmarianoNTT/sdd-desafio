from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from reembolso.io.cambio_io import ler_cambio
from reembolso.io.politica_io import ler_politica
from reembolso.motor.calcular import calcular_lote
from reembolso.motor.models import Colaborador, Despesa, Lote, Periodo, ResultadoLote


@pytest.fixture(scope="session")
def raiz_repo() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def politica_v4(raiz_repo):
    return ler_politica(raiz_repo / "exemplos" / "envelope" / "politica-v4.json")


@pytest.fixture(scope="session")
def cambio_v4(raiz_repo):
    return ler_cambio(raiz_repo / "exemplos" / "envelope" / "cambio.json")


def calcular(lote: Lote, politica_v4, cambio_v4) -> ResultadoLote:
    return calcular_lote(lote, politica_v4, cambio_v4)


@pytest.fixture
def calcular_lote_fn(politica_v4, cambio_v4):
    def _run(lote: Lote) -> ResultadoLote:
        return calcular_lote(lote, politica_v4, cambio_v4)

    return _run


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
        "moeda": "BRL",
    }
    defaults.update(kwargs)
    return Despesa(**defaults)


def lote_de_despesas(colaborador: Colaborador, periodo: Periodo, despesas: list[Despesa]) -> Lote:
    return Lote(colaborador=colaborador, periodo=periodo, despesas=despesas)
