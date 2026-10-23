from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from reembolso.motor.cambio import TabelaCambio


def cambio_de_dict(dados: dict[str, Any]) -> TabelaCambio:
    taxas: dict[str, dict[str, Decimal]] = {}
    for dia, moedas in dados.get("taxas", {}).items():
        taxas[dia] = {moeda: Decimal(str(valor)) for moeda, valor in moedas.items()}
    return TabelaCambio(taxas=taxas)


def ler_cambio(caminho: Path | str) -> TabelaCambio:
    path = Path(caminho)
    with path.open(encoding="utf-8") as fh:
        dados = json.load(fh)
    return cambio_de_dict(dados)
