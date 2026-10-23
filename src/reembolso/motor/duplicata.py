from __future__ import annotations

from datetime import date
from decimal import Decimal

from reembolso.motor.models import Despesa
from reembolso.motor.normalizacao import normalizar_categoria, normalizar_texto_comparacao


def chave_duplicata(despesa: Despesa, categoria_norm: str) -> tuple[date, str, str, Decimal, str]:
    return (
        despesa.data,
        categoria_norm,
        despesa.fornecedor.strip(),
        despesa.valor,
        normalizar_texto_comparacao(despesa.descricao),
    )


class RegistroDuplicatas:
    def __init__(self) -> None:
        self._vistos: set[tuple[date, str, str, Decimal, str]] = set()

    def registrar_ou_duplicata(self, despesa: Despesa, categoria_norm: str) -> bool:
        chave = chave_duplicata(despesa, categoria_norm)
        if chave in self._vistos:
            return True
        self._vistos.add(chave)
        return False
