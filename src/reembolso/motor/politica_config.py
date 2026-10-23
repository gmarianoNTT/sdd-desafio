from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class LimiteCategoria:
    limite: Decimal
    periodicidade: str


@dataclass(frozen=True)
class Politica:
    padrao: dict[str, LimiteCategoria]
    centros_custo: dict[str, dict[str, LimiteCategoria]]
    nota_fiscal_obrigatoria_acima_de: Decimal
    acrescimo_em_viagem_percentual: Decimal
    aprovacao_manual_acima_de: Decimal

    def mapa_efetivo(self, centro_custo: str) -> dict[str, LimiteCategoria]:
        base = dict(self.padrao)
        if centro_custo in self.centros_custo:
            base.update(self.centros_custo[centro_custo])
        return base

    def categoria_elegivel(self, centro_custo: str, categoria: str) -> bool:
        return categoria in self.mapa_efetivo(centro_custo)

    def limite(
        self,
        centro_custo: str,
        categoria: str,
        em_viagem: bool,
    ) -> Decimal | None:
        mapa = self.mapa_efetivo(centro_custo)
        if categoria not in mapa:
            return None
        cfg = mapa[categoria]
        limite = cfg.limite
        if em_viagem and cfg.periodicidade in ("dia", "diaria"):
            fator = Decimal("1") + self.acrescimo_em_viagem_percentual / Decimal("100")
            limite = limite * fator
        return limite

    def periodicidade(self, centro_custo: str, categoria: str) -> str | None:
        mapa = self.mapa_efetivo(centro_custo)
        if categoria not in mapa:
            return None
        return mapa[categoria].periodicidade
