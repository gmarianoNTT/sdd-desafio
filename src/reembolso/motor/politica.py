from decimal import Decimal

LIMITE_ALIMENTACAO = Decimal("60")
LIMITE_TRANSPORTE = Decimal("80")
LIMITE_HOSPEDAGEM_DIARIA = Decimal("250")
NF_VALOR_MINIMO_EXCLUSIVO = Decimal("100")
MULTIPLICADOR_VIAGEM = Decimal("1.5")

CATEGORIAS_PERMITIDAS = frozenset({"alimentacao", "transporte_urbano", "hospedagem"})
