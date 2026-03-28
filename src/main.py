# Grupo no Canvas: RA1 2

# Integrantes (ordem alfabética) e GitHub:
# - Gabriel Vidal Schneider (@Gabiru1089)
# - Lucca Fabricio Magalhães (@luccafm1)
# - Mohamad Kassem Diab (@Mo1409)
# - Vinícius Yamamoto Borges (@Vini-y)

import sys
import os
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

    for numero_linha, tokens in enumerate(tokens_por_linha, start=1):
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


def salvarAssembly(codigo_assembly, caminho="assembly/assembly.s"):
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


# Testes
def _teste_deve_falhar(nome_erro, linhas):
    print(f"  Esperado: {nome_erro}")
    try:
        exibirResultados(executarLinhas(tokenizarLinhas(linhas)))
        print("  [FALHOU] O programa não gerou erro quando deveria.")
        sys.exit(1)
    except SystemExit:
        print("  [OK] O programa gerou erro como esperado.")


def teste_memoria():
    """(V MEM) armazena, (MEM) recupera e sobrescreve o valor."""
    linhas = [
        "(100.0 SOMA)",
        "(SOMA)",
        "(200.0 SOMA)",
        "(SOMA)",
        "(50.0 BASE)",
        "(BASE)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_res():
    """(N RES) retorna resultados de linhas anteriores."""
    linhas = [
        "(7.0 3.0 +)",
        "(4.0 2.0 *)",
        "(1 RES)",
        "(2 RES)",
        "(3.0 3.0 ^)",
        "(1 RES)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_expressao():
    """Aninhamento, operações e uso de memória."""
    linhas = [
        "((1.5 2.0 +) (3.0 4.0 +) *)",
        "(10.0 BASE)",
        "((BASE 2.0 *) (5.0 1.0 -) +)",
        "((BASE 3.0 /) (2.0 4 ^) +)",
        "((9.0 3.0 //) (10.0 3.0 %) +)",
        "(BASE)",
        "((BASE 2 ^) (1 RES) -)",
        "(1 RES)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_divisao_por_zero():
    """Testa divisão por zero."""
    linhas = [
        "(10.0 0.0 /)",
    ]
    _teste_deve_falhar("divisão por zero", linhas)


def teste_memoria_nao_inicializada():
    """Testa memória não inicializada."""
    linhas = [
        "(MEM)",
    ]
    _teste_deve_falhar("memória não inicializada", linhas)


def teste_res_invalido():
    """Testa RES inválido."""
    linhas = [
        "(1 RES)",
    ]
    _teste_deve_falhar("RES inválido", linhas)


def teste_expressao_invalida():
    """Testa expressão inválida."""
    linhas = [
        "(10.0 5.0 + 3.0)",
    ]
    _teste_deve_falhar("expressão inválida", linhas)


def teste_erro_lexico():
    """Testa erro léxico."""
    linhas = [
        "(3.14.5 2.0 +)",
    ]
    _teste_deve_falhar("erro léxico", linhas)


def teste_operacoes_basicas():
    """Testa operações básicas isoladas."""
    linhas = [
        "(3.0 2.0 +)",
        "(10.0 5.0 -)",
        "(4.0 2.0 *)",
        "(9.0 3.0 /)",
        "(10.0 3.0 //)",
        "(10.0 3.0 %)",
        "(2.0 3.0 ^)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_memoria_em_expressao():
    """Testa uso de memória dentro de expressão."""
    linhas = [
        "(10.0 BASE)",
        "((BASE 2.0 *) (3.0 1.0 +) +)",
        "(BASE)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_res_em_expressao():
    """Testa uso de RES dentro de expressão aninhada."""
    linhas = [
        "(5.0 5.0 +)",
        "((1 RES) 2.0 *)",
        "((1 RES) (2 RES) +)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_linhas_vazias():
    """Testa se linhas vazias são ignoradas."""
    linhas = [
        "(3.0 2.0 +)",
        "",
        "   ",
        "(4.0 1.0 -)",
    ]
    exibirResultados(executarLinhas(tokenizarLinhas(linhas)))


def teste_divisao_inteira_por_zero():
    """Testa divisão inteira por zero."""
    linhas = [
        "(10.0 0.0 //)",
    ]
    _teste_deve_falhar("divisão inteira por zero", linhas)


def teste_modulo_por_zero():
    """Testa resto por zero."""
    linhas = [
        "(10.0 0.0 %)",
    ]
    _teste_deve_falhar("resto por zero", linhas)


def teste_res_zero():
    """Testa RES com zero."""
    linhas = [
        "(0 RES)",
    ]
    _teste_deve_falhar("RES zero", linhas)


def teste_res_negativo():
    """Testa RES negativo."""
    linhas = [
        "(-1 RES)",
    ]
    _teste_deve_falhar("RES negativo", linhas)


def teste_memoria_nao_inicializada_no_meio():
    """Testa memória não inicializada no meio do fluxo."""
    linhas = [
        "(7.0 3.0 +)",
        "(VALOR)",
        "(4.0 2.0 *)",
    ]
    _teste_deve_falhar("memória não inicializada no meio", linhas)


def teste_erro_lexico_no_meio():
    """Testa erro léxico no meio do fluxo."""
    linhas = [
        "(7.0 3.0 +)",
        "(3.14.5 2.0 +)",
        "(4.0 2.0 *)",
    ]
    _teste_deve_falhar("erro léxico no meio", linhas)

def executarTestes():
    print("Executando testes...\n")

    for nome, fn in [
        ("Comandos de memória", teste_memoria),
        ("Histórico com RES", teste_res),
        ("Expressão complexa", teste_expressao),
        ("Operações básicas", teste_operacoes_basicas),
        ("Memória em expressão", teste_memoria_em_expressao),
        ("RES em expressão", teste_res_em_expressao),
        ("Linhas vazias", teste_linhas_vazias),
        ("Divisão por zero", teste_divisao_por_zero),
        ("Divisão inteira por zero", teste_divisao_inteira_por_zero),
        ("Módulo por zero", teste_modulo_por_zero),
        ("Memória não inicializada", teste_memoria_nao_inicializada),
        ("Memória não inicializada no meio", teste_memoria_nao_inicializada_no_meio),
        ("RES inválido", teste_res_invalido),
        ("RES zero", teste_res_zero),
        ("RES negativo", teste_res_negativo),
        ("Expressão inválida", teste_expressao_invalida),
        ("Erro léxico", teste_erro_lexico),
        ("Erro léxico no meio", teste_erro_lexico_no_meio),
    ]:
        print(f"[TESTE] {nome}")
        fn()
        print()

    print("Todos os testes passaram.")

    
def main():
    linhas = lerArquivo()

    tokens_por_linha = tokenizarLinhas(linhas)

    salvarTokens(tokens_por_linha)

    resultados = executarLinhas(tokens_por_linha)

    exibirResultados(resultados)

    assembly = gerarAssembly(tokens_por_linha)

    salvarAssembly(assembly)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        executarTestes()
    else:
        main()