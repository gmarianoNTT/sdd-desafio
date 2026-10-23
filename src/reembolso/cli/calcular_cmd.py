from __future__ import annotations

from pathlib import Path

from reembolso.io.json_io import escrever_resultado, ler_lote
from reembolso.motor.calcular import calcular_lote


def run_calcular(input_path: str, output_path: str) -> int:
    try:
        lote = ler_lote(Path(input_path))
        resultado = calcular_lote(lote)
        escrever_resultado(Path(output_path), resultado)
    except FileNotFoundError:
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        return 1
    return 0
