import unicodedata


def normalizar_categoria(categoria_raw: str) -> str:
    texto = categoria_raw.strip().lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )


def normalizar_texto_comparacao(texto: str) -> str:
    compacto = " ".join(texto.strip().lower().split())
    return compacto
