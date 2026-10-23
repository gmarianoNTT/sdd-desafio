from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Colaborador:
    id: str
    nome: str
    centro_custo: str


@dataclass(frozen=True)
class Periodo:
    competencia: str
    inicio: date
    fim: date


@dataclass(frozen=True)
class Despesa:
    id: str
    data: date
    categoria_raw: str
    descricao: str
    fornecedor: str
    valor: Decimal
    tem_nota_fiscal: bool


@dataclass(frozen=True)
class Lote:
    colaborador: Colaborador
    periodo: Periodo
    despesas: list[Despesa]


@dataclass(frozen=True)
class ResultadoItem:
    id: str
    valor_informado: Decimal
    valor_reembolsavel: Decimal
    status: str
    justificativa: str


@dataclass(frozen=True)
class ResultadoLote:
    colaborador_id: str
    competencia: str
    itens: list[ResultadoItem]
    total_informado: Decimal
    total_reembolsavel: Decimal
