from typing import Any, Iterable, List, Optional, Union

def formatarValor(valor: Any) -> str:
    """Formata um valor numérico com uma casa decimal."""
    if isinstance(valor, (int, float)):
        return f"{float(valor):.1f}"
    if valor is None:
        return "<pendente>"
    return str(valor)

def exibirResultados(resultados: Optional[Iterable[Union[int, float, None]]]) -> List[str]:
    """Exibe os resultados das expressões avaliadas."""
    if resultados is None:
        print("Nenhum resultado para exibir.")
        return []

    lista = list(resultados)
    if not lista:
        print("Nenhum resultado para exibir.")
        return []

    linhas = ["Resultados:"]
    for indice, valor in enumerate(lista, start=1):
        linhas.append(f"[{indice:02d}] {formatarValor(valor)}")

    for linha in linhas:
        print(linha)

    return linhas