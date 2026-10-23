from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


@dataclass(frozen=True)
class TabelaCambio:
    taxas: dict[str, dict[str, Decimal]]
    max_retrocesso_dias: int = 10

    def taxa_para(self, data: date, moeda: str) -> Decimal | None:
        if moeda == "BRL":
            return Decimal("1")
        atual = data
        for _ in range(self.max_retrocesso_dias + 1):
            chave = atual.isoformat()
            dia = self.taxas.get(chave)
            if dia is not None and moeda in dia:
                return dia[moeda]
            atual -= timedelta(days=1)
        return None
