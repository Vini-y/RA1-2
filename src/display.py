# Grupo no Canvas: RA1 2

# Integrantes (ordem alfabética) e GitHub:
# - Gabriel Vidal Schneider (@Gabiru1089)
# - Lucca Fabricio Magalhães (@luccafm1)
# - Mohamad Kassem Diab (@Mo1409)
# - Vinícius Yamamoto Borges (@Vini-y)

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


# --- Funções de teste ---

def teste_exibirResultados():
    """
    Testa exibirResultados com o fluxo completo do programa:
    tokenização, execução e exibição dos resultados.
    Verifica formatação com 1 casa decimal, lista vazia e None.
    """
    from lexer import parseExpressao
    from executor import executarExpressao

    # Testa fluxo completo: tokenizar -> executar -> exibir
    expressoes = [
        "(5.5 1.5 +)",
        "(12 7 -)",
        "(3.5 6.0 *)",
        "(18.0 5.0 /)",
        "(25 4 //)",
        "(25 4 %)",
        "(3.0 5 ^)",
    ]
    memoria = {}
    historico = []
    resultados = []

    for expr in expressoes:
        tokens = []
        parseExpressao(expr, tokens)
        res = executarExpressao(tokens, memoria, historico)
        resultados.append(res)

    linhas = exibirResultados(resultados)

    assert linhas[0] == "Resultados:", f"Cabeçalho inesperado: {linhas[0]}"
    assert len(linhas) == len(resultados) + 1, "Número de linhas não corresponde"

    # Verifica formatação com 1 casa decimal
    assert "[01] 7.0" in linhas[1], f"Resultado da adição inesperado: {linhas[1]}"
    assert "[02] 5.0" in linhas[2], f"Resultado da subtração inesperado: {linhas[2]}"
    assert "[03] 21.0" in linhas[3], f"Resultado da multiplicação inesperado: {linhas[3]}"
    assert "[04] 3.6" in linhas[4], f"Resultado da divisão inesperado: {linhas[4]}"
    assert "[05] 6.0" in linhas[5], f"Resultado da divisão inteira inesperado: {linhas[5]}"
    assert "[06] 1.0" in linhas[6], f"Resultado do resto inesperado: {linhas[6]}"
    assert "[07] 243.0" in linhas[7], f"Resultado da potência inesperado: {linhas[7]}"

    # Testa lista vazia
    linhas_vazio = exibirResultados([])
    assert linhas_vazio == [], "Lista vazia deve retornar []"

    # Testa None
    linhas_none = exibirResultados(None)
    assert linhas_none == [], "None deve retornar []"

    print("[PASS] teste_exibirResultados")


if __name__ == "__main__":
    teste_exibirResultados()