from __future__ import annotations

from datetime import date
from decimal import Decimal

from reembolso.motor.duplicata import RegistroDuplicatas
from reembolso.motor.hospedagem import extrair_numero_diarias
from reembolso.motor.models import Despesa, Lote, ResultadoItem, ResultadoLote
from reembolso.motor.monetario import arredondar_moeda
from reembolso.motor.normalizacao import normalizar_categoria
from reembolso.motor.politica import (
    CATEGORIAS_PERMITIDAS,
    LIMITE_ALIMENTACAO,
    LIMITE_HOSPEDAGEM_DIARIA,
    LIMITE_TRANSPORTE,
    MULTIPLICADOR_VIAGEM,
    NF_VALOR_MINIMO_EXCLUSIVO,
)
from reembolso.motor.viagem import datas_em_viagem

SaldoKey = tuple[date, str]


def _limite_diario_categoria(categoria: str, em_viagem: bool) -> Decimal:
    if categoria == "alimentacao":
        base = LIMITE_ALIMENTACAO
    elif categoria == "transporte_urbano":
        base = LIMITE_TRANSPORTE
    else:
        raise ValueError(f"limite diário não aplicável a {categoria}")
    if em_viagem:
        return base * MULTIPLICADOR_VIAGEM
    return base


def _limite_hospedagem_diaria(em_viagem: bool) -> Decimal:
    if em_viagem:
        return LIMITE_HOSPEDAGEM_DIARIA * MULTIPLICADOR_VIAGEM
    return LIMITE_HOSPEDAGEM_DIARIA


def _status_de(valor_bruto: Decimal, valor_reembolsavel: Decimal) -> str:
    informado = arredondar_moeda(valor_bruto)
    if valor_reembolsavel == 0:
        return "recusado"
    if valor_reembolsavel < informado:
        return "parcial"
    return "aprovado"


def _item_recusado(despesa: Despesa, justificativa: str) -> ResultadoItem:
    informado = arredondar_moeda(despesa.valor)
    return ResultadoItem(
        id=despesa.id,
        valor_informado=informado,
        valor_reembolsavel=Decimal("0"),
        status="recusado",
        justificativa=justificativa,
    )


def _dentro_competencia(despesa: Despesa, lote: Lote) -> bool:
    return lote.periodo.inicio <= despesa.data <= lote.periodo.fim


def _requer_nf_recusada(despesa: Despesa) -> bool:
    return despesa.valor > NF_VALOR_MINIMO_EXCLUSIVO and not despesa.tem_nota_fiscal


def _calcular_hospedagem(despesa: Despesa, em_viagem: bool) -> Decimal:
    n = extrair_numero_diarias(despesa.descricao)
    valor_por_diaria = despesa.valor / n
    teto = _limite_hospedagem_diaria(em_viagem)
    total = Decimal("0")
    for _ in range(n):
        total += min(valor_por_diaria, teto)
    return min(total, despesa.valor)


def _consumir_saldo_diario(
    saldos: dict[SaldoKey, Decimal],
    chave: SaldoKey,
    limite: Decimal,
    valor: Decimal,
) -> Decimal:
    restante = saldos.get(chave, limite)
    aprovado = min(valor, restante)
    saldos[chave] = restante - aprovado
    return aprovado


def calcular_lote(lote: Lote) -> ResultadoLote:
    viagem = datas_em_viagem(lote.despesas)
    duplicatas = RegistroDuplicatas()
    saldos: dict[SaldoKey, Decimal] = {}
    itens: list[ResultadoItem] = []

    for despesa in lote.despesas:
        categoria = normalizar_categoria(despesa.categoria_raw)

        if duplicatas.registrar_ou_duplicata(despesa, categoria):
            itens.append(_item_recusado(despesa, "Despesa duplicada; apenas a primeira ocorrência é elegível."))
            continue

        if not _dentro_competencia(despesa, lote):
            itens.append(
                _item_recusado(despesa, "Data fora do período de competência informado.")
            )
            continue

        if categoria not in CATEGORIAS_PERMITIDAS:
            itens.append(_item_recusado(despesa, "Categoria não coberta pela política de reembolso."))
            continue

        if _requer_nf_recusada(despesa):
            itens.append(
                _item_recusado(
                    despesa,
                    "Nota fiscal obrigatória para despesas com valor acima de R$ 100,00.",
                )
            )
            continue

        if despesa.valor < 0:
            chave = (despesa.data, categoria)
            limite = _limite_diario_categoria(categoria, despesa.data in viagem)
            saldos[chave] = saldos.get(chave, limite) + abs(despesa.valor)
            itens.append(
                ResultadoItem(
                    id=despesa.id,
                    valor_informado=arredondar_moeda(despesa.valor),
                    valor_reembolsavel=Decimal("0"),
                    status="recusado",
                    justificativa="Estorno registrado; margem devolvida ao limite diário da categoria.",
                )
            )
            continue

        em_viagem = despesa.data in viagem

        if categoria == "hospedagem":
            bruto = _calcular_hospedagem(despesa, em_viagem)
            reembolso = arredondar_moeda(bruto)
            justificativa = "Hospedagem rateada por diária conforme teto da política."
            if reembolso < despesa.valor:
                justificativa = (
                    "Hospedagem rateada por diária; reembolso parcial por teto por diária."
                )
            itens.append(
                ResultadoItem(
                    id=despesa.id,
                    valor_informado=arredondar_moeda(despesa.valor),
                    valor_reembolsavel=reembolso,
                    status=_status_de(despesa.valor, reembolso),
                    justificativa=justificativa,
                )
            )
            continue

        limite = _limite_diario_categoria(categoria, em_viagem)
        chave = (despesa.data, categoria)
        bruto = _consumir_saldo_diario(saldos, chave, limite, despesa.valor)
        reembolso = arredondar_moeda(bruto)

        if reembolso == 0:
            justificativa = "Limite diário da categoria esgotado para esta data."
        elif reembolso < despesa.valor:
            justificativa = (
                f"Limite diário de {categoria.replace('_', ' ')}; reembolso parcial do excedente."
            )
        else:
            justificativa = "Despesa aprovada dentro da política."

        itens.append(
            ResultadoItem(
                id=despesa.id,
                valor_informado=arredondar_moeda(despesa.valor),
                valor_reembolsavel=reembolso,
                status=_status_de(despesa.valor, reembolso),
                justificativa=justificativa,
            )
        )

    total_informado = sum((i.valor_informado for i in itens), Decimal("0"))
    total_reembolsavel = sum((i.valor_reembolsavel for i in itens), Decimal("0"))
    return ResultadoLote(
        colaborador_id=lote.colaborador.id,
        competencia=lote.periodo.competencia,
        itens=itens,
        total_informado=arredondar_moeda(total_informado),
        total_reembolsavel=arredondar_moeda(total_reembolsavel),
    )
