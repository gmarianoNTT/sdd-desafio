from pathlib import Path

from reembolso.io.json_io import ler_lote


def test_io_le_lote_exemplo():
    raiz = Path(__file__).resolve().parents[1]
    lote = ler_lote(raiz / "exemplos" / "despesas-exemplo.json")
    assert lote.colaborador.id == "c-0417"
    assert lote.periodo.competencia == "2026-07"
    assert len(lote.despesas) == 14
    assert lote.despesas[0].id == "d-001"
