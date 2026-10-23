from decimal import Decimal, ROUND_HALF_UP

DUAS_CASAS = Decimal("0.01")


def arredondar_moeda(valor: Decimal) -> Decimal:
    return valor.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)


def decimal_de_entrada(valor: float | int | str) -> Decimal:
    return Decimal(str(valor))
