from typing import Iterable, List

def formatar_valor(valor) -> str:
    """Formata um valor numerico com uma casa decimal."""
    if isinstance(valor, (int, float)):
        return f"{float(valor):.1f}"
    if valor is None:
        return "<pendente>"
    return str(valor)