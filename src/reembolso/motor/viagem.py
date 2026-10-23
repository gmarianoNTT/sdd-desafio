from __future__ import annotations

from datetime import date, timedelta

from reembolso.motor.hospedagem import extrair_numero_diarias
from reembolso.motor.models import Despesa
from reembolso.motor.normalizacao import normalizar_categoria


def datas_em_viagem(despesas: list[Despesa]) -> set[date]:
    datas: set[date] = set()
    for despesa in despesas:
        if normalizar_categoria(despesa.categoria_raw) != "hospedagem":
            continue
        n = extrair_numero_diarias(despesa.descricao)
        for offset in range(n):
            datas.add(despesa.data + timedelta(days=offset))
    return datas
