import json
import subprocess
import sys
from pathlib import Path


def test_cli_calcular_arquivo(tmp_path):
    raiz = Path(__file__).resolve().parents[1]
    entrada = raiz / "exemplos" / "despesas-exemplo.json"
    politica = raiz / "exemplos" / "envelope" / "politica-v4.json"
    cambio = raiz / "exemplos" / "envelope" / "cambio.json"
    saida = tmp_path / "resultado.json"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "reembolso.cli.main",
            "calcular",
            "--input",
            str(entrada),
            "--output",
            str(saida),
            "--politica",
            str(politica),
            "--cambio",
            str(cambio),
        ],
        cwd=raiz,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    dados = json.loads(saida.read_text(encoding="utf-8"))
    assert dados["colaborador"]["id"] == "c-0417"
    assert len(dados["itens"]) == 14
