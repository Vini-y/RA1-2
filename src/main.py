import sys
from lexer import parseExpressao, LexError
from assembly import lerArquivo, gerarAssembly
from display import exibirResultados
#from executor import executarExpressao


def tokenizarLinhas(linhas):
    """
    Percorre cada linha do arquivo fonte e chama parseExpressao.
    Retorna uma lista de listas de tokens (tokens por linha).
    """
    tokens_por_linha = []

    for numero_linha, linha in enumerate(linhas, start=1):
        if not linha.strip():
            continue

        tokenslinha = []
        try:
            parseExpressao(linha, tokenslinha)
        except LexError as e:
            print(f"Erro léxico na linha {numero_linha}: {e}", file=sys.stderr)
            sys.exit(1)

        tokens_por_linha.append(tokenslinha)

    return tokens_por_linha



