# Integrantes (ordem alfabética) e GitHub:
# - Gabriel Vidal Schneider (@Gabiru1089)
# - Lucca Fabricio Magalhães (@luccafm1)
# - Mohamad Kassem Diab (@Mo1409)
# - Vinícius Yamamoto Borges (@Vini-y)

# Grupo no Canvas: RA1 2

import sys
from lexer import parseExpressao, LexError
from assembly import lerArquivo, gerarAssembly
from display import exibirResultados
from executor import executarExpressao, ErroExpressaoInvalida, ErroDivisaoPorZero, ErroMemoriaNaoInicializada, ErroHistoricoInvalido


def tokenizarLinhas(linhas):
    """
    Percorre cada linha do arquivo fonte e chama parseExpressao.
    Retorna uma lista de listas de tokens (tokens por linha).
    Linhas em branco são ignoradas.
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

def executarLinhas(tokens_por_linha):
    """
    Executa cada linha de tokens via executarExpressao, mantendo
    memória e histórico compartilhados entre todas as linhas do arquivo.

    Retorna a lista de resultados (float), na mesma ordem das linhas.
    O histórico segue a convenção do executor: índice 0 = resultado
    mais recente, portanto (1 RES) acessa o resultado da linha anterior.
    """
    memoria   = {}
    historico = []
    resultados = []

    for numero_linha, tokens in enumerate(tokens_por_linha, start=0):
        try:
            resultado = executarExpressao(tokens, memoria, historico)
            resultados.append(resultado)
        except ErroDivisaoPorZero as e:
            print(f"Erro na linha {numero_linha}: divisão por zero — {e}",
                  file=sys.stderr)
            sys.exit(1)
        except ErroMemoriaNaoInicializada as e:
            print(f"Erro na linha {numero_linha}: memória não inicializada — {e}",
                  file=sys.stderr)
            sys.exit(1)
        except ErroHistoricoInvalido as e:
            print(f"Erro na linha {numero_linha}: RES inválido — {e}",
                  file=sys.stderr)
            sys.exit(1)
        except ErroExpressaoInvalida as e:
            print(f"Erro na linha {numero_linha}: expressão inválida — {e}",
                  file=sys.stderr)
            sys.exit(1)

    return resultados

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


def main():
    linhas = lerArquivo()

    tokens_por_linha = tokenizarLinhas(linhas)

    salvarTokens(tokens_por_linha)

    resultados = executarLinhas(tokens_por_linha)

    exibirResultados(resultados)

    assembly = gerarAssembly(tokens_por_linha)

    salvarAssembly(assembly)


if __name__ == "__main__":
    main()
