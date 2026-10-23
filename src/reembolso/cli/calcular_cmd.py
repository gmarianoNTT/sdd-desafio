from __future__ import annotations

from pathlib import Path

from reembolso.io.cambio_io import ler_cambio
from reembolso.io.json_io import escrever_resultado, ler_lote
from reembolso.io.politica_io import ler_politica
from reembolso.motor.calcular import calcular_lote


def run_calcular(
    input_path: str,
    output_path: str,
    politica_path: str,
    cambio_path: str,
) -> int:
    try:
        lote = ler_lote(Path(input_path))
        politica = ler_politica(Path(politica_path))
        cambio = ler_cambio(Path(cambio_path))
        resultado = calcular_lote(lote, politica, cambio)
        escrever_resultado(Path(output_path), resultado)
    except FileNotFoundError:
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        return 1
    return 0
