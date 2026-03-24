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


def salvarTokens(tokens_por_linha, caminho="tokens.txt"):
    """Salva os tokens da última execução em tokens.txt"""
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("tipo,valor,posicao\n")
            for tokenslinha in tokens_por_linha:
                for tipo, valor, pos in tokenslinha:
                    f.write(f"{tipo},{valor},{pos}\n")
        print(f"Tokens salvos em '{caminho}'.")
    except OSError as e:
        print(f"Erro ao salvar tokens: {e}", file=sys.stderr)


def salvarAssembly(codigo_assembly, caminho="assembly.s"):
    """Grava o código Assembly gerado em disco"""
    if not codigo_assembly:
        print("gerarAssembly não retornou código.")
        return
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(codigo_assembly)
        print(f"\nAssembly gerado em '{caminho}'.")
    except OSError as e:
        print(f"Erro ao salvar Assembly: {e}", file=sys.stderr)
        sys.exit(1)


