from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

from reembolso.motor.models import Colaborador, Despesa, Lote, Periodo, ResultadoLote
from reembolso.motor.monetario import arredondar_moeda, decimal_de_entrada


def _parse_date(texto: str) -> date:
    return date.fromisoformat(texto)


def lote_de_dict(dados: dict[str, Any]) -> Lote:
    colab = dados["colaborador"]
    periodo = dados["periodo"]
    despesas = [
        Despesa(
            id=item["id"],
            data=_parse_date(item["data"]),
            categoria_raw=item["categoria"],
            descricao=item["descricao"],
            fornecedor=item["fornecedor"],
            valor=decimal_de_entrada(item["valor"]),
            tem_nota_fiscal=bool(item["tem_nota_fiscal"]),
            moeda=str(item.get("moeda", "BRL")).upper(),
        )
        for item in dados["despesas"]
    ]
    return Lote(
        colaborador=Colaborador(
            id=colab["id"],
            nome=colab["nome"],
            centro_custo=colab["centro_custo"],
        ),
        periodo=Periodo(
            competencia=periodo["competencia"],
            inicio=_parse_date(periodo["inicio"]),
            fim=_parse_date(periodo["fim"]),
        ),
        despesas=despesas,
    )


def _decimal_para_json(valor: Decimal) -> float:
    return float(arredondar_moeda(valor))


def resultado_para_dict(resultado: ResultadoLote) -> dict[str, Any]:
    return {
        "colaborador": {"id": resultado.colaborador_id},
        "periodo": {"competencia": resultado.competencia},
        "itens": [
            {
                "id": item.id,
                "valor_informado": _decimal_para_json(item.valor_informado),
                "valor_reembolsavel": _decimal_para_json(item.valor_reembolsavel),
                "status": item.status,
                "justificativa": item.justificativa,
            }
            for item in resultado.itens
        ],
        "resumo": {
            "total_informado": _decimal_para_json(resultado.total_informado),
            "total_reembolsavel": _decimal_para_json(resultado.total_reembolsavel),
        },
    }


def ler_lote(caminho: Path | str) -> Lote:
    path = Path(caminho)
    with path.open(encoding="utf-8") as fh:
        dados = json.load(fh)
    return lote_de_dict(dados)


def escrever_resultado(caminho: Path | str, resultado: ResultadoLote) -> None:
    path = Path(caminho)
    payload = resultado_para_dict(resultado)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

