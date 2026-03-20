# Leitura de arquivo e gerador de Assembly ARMv7

import sys

def lerArquivo():
    """
    Lê o arquivo passado via argumento de linha de comando linha a linha
    e retorna lista de strings (uma por linha, sem '\n').
    """
    if len(sys.argv) < 2:
        print("Erro: nenhum arquivo fornecido. Passe um arquivo como parametro", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    try:
        with open(path, "r", encoding="utf-8") as f:
            linhas = [linha.rstrip("\n") for linha in f]

    except FileNotFoundError:
        print(f"Erro: arquivo '{path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    except OSError as e:
        print(f"Erro ao abrir '{path}': {e}", file=sys.stderr)
        sys.exit(1)

    return linhas

def gerarAssembly():
    pass