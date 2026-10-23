from __future__ import annotations

from datetime import date
from decimal import Decimal

from reembolso.motor.cambio import TabelaCambio
from reembolso.motor.duplicata import RegistroDuplicatas
from reembolso.motor.hospedagem import extrair_numero_diarias
from reembolso.motor.models import Despesa, Lote, ResultadoItem, ResultadoLote
from reembolso.motor.monetario import arredondar_moeda
from reembolso.motor.normalizacao import normalizar_categoria
from reembolso.motor.politica_config import Politica
from reembolso.motor.viagem import datas_em_viagem

SaldoKey = tuple[date, str]


def _converter_brl(
    despesa: Despesa, cambio: TabelaCambio
) -> tuple[Decimal | None, str | None]:
    taxa = cambio.taxa_para(despesa.data, despesa.moeda)
    if taxa is None:
        return None, "Cotação indisponível para a moeda na data da despesa."
    return arredondar_moeda(despesa.valor * taxa), None


def _status_de(valor_brl_elegivel: Decimal, valor_reembolsavel: Decimal) -> str:
    elegivel = arredondar_moeda(valor_brl_elegivel)
    if valor_reembolsavel == 0:
        return "recusado"
    if valor_reembolsavel < elegivel:
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


def _requer_nf_recusada(valor_brl: Decimal, despesa: Despesa, politica: Politica) -> bool:
    return (
        valor_brl > politica.nota_fiscal_obrigatoria_acima_de
        and not despesa.tem_nota_fiscal
    )


def _calcular_hospedagem(
    valor_brl: Decimal, descricao: str, teto_diaria: Decimal
) -> Decimal:
    n = extrair_numero_diarias(descricao)
    valor_por_diaria = valor_brl / n
    total = Decimal("0")
    for _ in range(n):
        total += min(valor_por_diaria, teto_diaria)
    return min(total, valor_brl)


def _consumir_saldo_diario(
    saldos: dict[SaldoKey, Decimal],
    chave: SaldoKey,
    limite: Decimal,
    valor_brl: Decimal,
) -> Decimal:
    restante = saldos.get(chave, limite)
    aprovado = min(valor_brl, restante)
    saldos[chave] = restante - aprovado
    return aprovado


def calcular_lote(lote: Lote, politica: Politica, cambio: TabelaCambio) -> ResultadoLote:
    cc = lote.colaborador.centro_custo
    viagem = datas_em_viagem(lote.despesas)
    duplicatas = RegistroDuplicatas()
    saldos: dict[SaldoKey, Decimal] = {}
    itens: list[ResultadoItem] = []

    for despesa in lote.despesas:
        categoria = normalizar_categoria(despesa.categoria_raw)
        informado = arredondar_moeda(despesa.valor)

        if duplicatas.registrar_ou_duplicata(despesa, categoria):
            itens.append(_item_recusado(despesa, "Despesa duplicada; apenas a primeira ocorrência é elegível."))
            continue

        if not _dentro_competencia(despesa, lote):
            itens.append(
                _item_recusado(despesa, "Data fora do período de competência informado.")
            )
            continue

        valor_brl, erro_cambio = _converter_brl(despesa, cambio)
        if valor_brl is None:
            itens.append(_item_recusado(despesa, erro_cambio or "Cotação indisponível."))
            continue

        if not politica.categoria_elegivel(cc, categoria):
            itens.append(_item_recusado(despesa, "Categoria não coberta pela política de reembolso."))
            continue

        if _requer_nf_recusada(valor_brl, despesa, politica):
            itens.append(
                _item_recusado(
                    despesa,
                    "Nota fiscal obrigatória para despesas com valor acima de R$ 100,00.",
                )
            )
            continue

        if despesa.valor < 0:
            em_viagem = despesa.data in viagem
            limite = politica.limite(cc, categoria, em_viagem)
            if limite is None or politica.periodicidade(cc, categoria) != "dia":
                itens.append(_item_recusado(despesa, "Estorno não aplicável a esta categoria."))
                continue
            chave = (despesa.data, categoria)
            saldos[chave] = saldos.get(chave, limite) + abs(valor_brl)
            itens.append(
                ResultadoItem(
                    id=despesa.id,
                    valor_informado=informado,
                    valor_reembolsavel=Decimal("0"),
                    status="recusado",
                    justificativa="Estorno registrado; margem devolvida ao limite diário da categoria.",
                )
            )
            continue

        em_viagem = despesa.data in viagem
        teto = politica.limite(cc, categoria, em_viagem)
        if teto is None:
            itens.append(_item_recusado(despesa, "Categoria não coberta pela política de reembolso."))
            continue

        periodicidade = politica.periodicidade(cc, categoria)

        if categoria == "hospedagem" and periodicidade == "diaria":
            bruto = _calcular_hospedagem(valor_brl, despesa.descricao, teto)
            reembolso = arredondar_moeda(bruto)
            if teto == 0:
                justificativa = "Hospedagem não reembolsável para este centro de custo."
            elif reembolso < valor_brl:
                justificativa = (
                    "Hospedagem rateada por diária; reembolso parcial por teto por diária."
                )
            else:
                justificativa = "Hospedagem rateada por diária conforme teto da política."
            itens.append(
                ResultadoItem(
                    id=despesa.id,
                    valor_informado=informado,
                    valor_reembolsavel=reembolso,
                    status=_status_de(valor_brl, reembolso),
                    justificativa=justificativa,
                )
            )
            continue

        if periodicidade == "dia":
            chave = (despesa.data, categoria)
            bruto = _consumir_saldo_diario(saldos, chave, teto, valor_brl)
            reembolso = arredondar_moeda(bruto)

            if reembolso == 0:
                justificativa = "Limite diário da categoria esgotado para esta data."
            elif reembolso < valor_brl:
                justificativa = (
                    f"Limite diário de {categoria.replace('_', ' ')}; reembolso parcial do excedente."
                )
            else:
                justificativa = "Despesa aprovada dentro da política."

            itens.append(
                ResultadoItem(
                    id=despesa.id,
                    valor_informado=informado,
                    valor_reembolsavel=reembolso,
                    status=_status_de(valor_brl, reembolso),
                    justificativa=justificativa,
                )
            )
            continue

        itens.append(_item_recusado(despesa, "Periodicidade de limite não suportada."))

    total_informado = sum((i.valor_informado for i in itens), Decimal("0"))
    total_reembolsavel = sum((i.valor_reembolsavel for i in itens), Decimal("0"))
    return ResultadoLote(
        colaborador_id=lote.colaborador.id,
        competencia=lote.periodo.competencia,
        itens=itens,
        total_informado=arredondar_moeda(total_informado),
        total_reembolsavel=arredondar_moeda(total_reembolsavel),
    )
