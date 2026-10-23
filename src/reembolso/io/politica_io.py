from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from reembolso.motor.politica_config import LimiteCategoria, Politica


def _limites_de_bloco(bloco: dict[str, Any]) -> dict[str, LimiteCategoria]:
    resultado: dict[str, LimiteCategoria] = {}
    for categoria, cfg in bloco.items():
        resultado[categoria] = LimiteCategoria(
            limite=Decimal(str(cfg["limite"])),
            periodicidade=str(cfg["periodicidade"]),
        )
    return resultado


def politica_de_dict(dados: dict[str, Any]) -> Politica:
    centros: dict[str, dict[str, LimiteCategoria]] = {}
    for cc, bloco in dados.get("centros_custo", {}).items():
        centros[cc] = _limites_de_bloco(bloco)
    return Politica(
        padrao=_limites_de_bloco(dados["padrao"]),
        centros_custo=centros,
        nota_fiscal_obrigatoria_acima_de=Decimal(
            str(dados["nota_fiscal_obrigatoria_acima_de"])
        ),
        acrescimo_em_viagem_percentual=Decimal(
            str(dados["acrescimo_em_viagem_percentual"])
        ),
    )


def ler_politica(caminho: Path | str) -> Politica:
    path = Path(caminho)
    with path.open(encoding="utf-8") as fh:
        dados = json.load(fh)
    return politica_de_dict(dados)
