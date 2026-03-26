from typing import Iterable


def formatar_valor(valor: float | None) -> str:
    """Formata um valor numérico com duas casas decimais."""
    if isinstance(valor, (int, float)):
        return f"{float(valor):.1f}"
    if valor is None:
        return "<pendente>"
    raise TypeError(f"Valor invalido para exibicao: {valor!r}")


def exibirResultados(resultados: Iterable[float | None] | None) -> list[str]:
    """Exibe os resultados das expressões avaliadas."""
    if resultados is None:
        print("Nenhum resultado para exibir.")
        return []

    lista_resultados = list(resultados)
    if not lista_resultados:
        print("Nenhum resultado para exibir.")
        return []

    linhas: list[str] = ["Resultados:"]
    for indice, valor in enumerate(lista_resultados, start=1):
        linhas.append(f"[{indice:02d}] {formatar_valor(valor)}")

    for linha in linhas:
        print(linha)

    return linhas