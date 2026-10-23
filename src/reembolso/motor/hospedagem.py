import re

_REGEX_DIARIAS = re.compile(r"\b(\d+)\s*(diarias?|noites?)\b", re.IGNORECASE)


def extrair_numero_diarias(descricao: str) -> int:
    match = _REGEX_DIARIAS.search(descricao)
    if match:
        return int(match.group(1))
    return 1
