from typing import Iterable, List

def formatar_valor(valor) -> str:
    """Formata um valor numerico com uma casa decimal."""
    if isinstance(valor, (int, float)):
        return f"{float(valor):.1f}"
    if valor is None:
        return "<pendente>"
    return str(valor)

def exibirResultados(resultados: Iterable[float]) -> List[str]:
    """Exibe os resultados das expressoes avaliadas."""
    if resultados is None:
        print("Nenhum resultado para exibir.")
        return []

    lista = list(resultados)
    if not lista:
        print("Nenhum resultado para exibir.")
        return []

    linhas = ["Resultados:"]
    for indice, valor in enumerate(lista, start=1):
        linhas.append(f"[{indice:02d}] {formatar_valor(valor)}")

    for linha in linhas:
        print(linha)

    return linhas