# Executor de expressões RPN e gerenciamento de memória
from lexer import parseExpressao, LexError

"""
executarExpressao.py

Avalia as expressões produzidas em lexer.py

Formato do Token esperado: tupla (tipo, valor, posição)
    ("NUM", "3.14", 2)
    ("OP", "+", 7)
    ("LPAREN", "(", 0)
    ("RPAREN", ")", 9)
    ("RES", "RES", 5)
    ("MEM", "VAR", 3)

Depende de:
    lexer.py -> parseExpressao, LexError

"""

# Constantes - tipos de token do lexer

T_NUM = "NUM"
T_OP = "OP"
T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"
T_RES ="RES"
T_MEM = "MEM"

# Funções para auxiliar na identificaçãomdos itens do token

def tipo(token: tuple) -> str:
    return token[0]

def valor(token: tuple) -> str:
    return token[1]

def posicao(token: tuple) -> int:
    return token[2]

# Exceções específicas de execução

class ErroDivisaoPorZero(Exception):
    pass

class ErroExpressaoInvalida(Exception):
    pass

class ErroMemoriaNaoInicializada(Exception):
    pass
class ErroHistoricoInvalido(Exception):
    pass

#Converter linha em tokens utilizando o lexer

def tokenizar(linha : str) -> str:
    """Chama a parseExpressao do Lexer e retorna lista de de tokens
        propaga LexError se tiverem símbolos inválidos
    """

    tokens = []
    parseExpressao(linha, tokens)
    return tokens

def encontrar_fechamento(tokens: list, inicio: int) -> int:
    """
    tokens[inicio] é um LPAREN, a função retorna o RPAREN
    correspondente (mesmo nível de profundidade)
    """
    profundidade = 0
    i = inicio

    while i < len(tokens):
        if tipo(tokens[i]) == T_LPAREN:
            profundidade += 1
        elif tipo(tokens[i]) == T_RPAREN:
            profundidade -= 1
            if profundidade == 0:
                return i
        i += 1
    raise ErroExpressaoInvalida(
        f"Parêntese aberto na posição {posicao(tokens[inicio])} não foi fechado!"
    )

def _aplicar_operador(op: str, a: float, b: float) -> float:
    """
    Aplicar operador sobre 2 floats 
    """
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0.0:
            raise ErroDivisaoPorZero(f"Divisão real por zero: {a} / {b}")
        return a/ b
    if op =='//':
        if b == 0:
            raise ErroDivisaoPorZero(f"Divisão inteira por zero: {a} / {b}")
        return float(int(a) // int(b))
    if op == "%":
        if b == 0:
            raise ErroDivisaoPorZero(f"Resto por zero: {a} % {b}")
        return float(int(a) % int(b))
    if op == "^":
        exp = int(b)
        if exp < 0:
            raise ErroExpressaoInvalida(
                f"Expoente deve ser inteiro positivo, recebeu {b}"
            )
        return float(a ** exp)
    raise ErroExpressaoInvalida(f"Operador '{op}' desconhecido")

# Avaliador de expressão plana (sem aninhamento)

def _avaliar_expressao_plana(tokens: list, memoria: dict, historico: list) -> float:
    """
    Avalia uma expressão RPN plana (sem LPAREN internos) usando pilha.
 
    Detecta o tipo de expressão pelo conteúdo interno:
      ( MEM )       -> leitura de memória
      ( NUM RES )   -> histórico
      ( NUM MEM )   -> escrita em memória
      ( NUM... OP ) -> aritmética RPN
    """
    # Remove parênteses externos
    if tipo(tokens[0]) == T_LPAREN and tipo(tokens[-1]) == T_RPAREN:
        interior = tokens[1:-1]
    else:
        raise ErroExpressaoInvalida(
            "Expressão deve começar com '(' e terminar com ')'"
        )
 
    # (MEM) — leitura de variável
    if len(interior) == 1 and tipo(interior[0]) == T_MEM:
        nome = valor(interior[0])
        if nome not in memoria:
            raise ErroMemoriaNaoInicializada(
                f"Memória '{nome}' não foi inicializada"
            )
        return memoria[nome]
 
    # (NUM RES) — retorna resultado N linhas anteriores
    if (len(interior) == 2 and
            tipo(interior[0]) == T_NUM and
            tipo(interior[1]) == T_RES):
        n = int(float(valor(interior[0])))
        if n < 0:
            raise ErroHistoricoInvalido(
                f"N em (N RES) deve ser não negativo, recebeu: {n}"
            )
        if n >= len(historico):
            raise ErroHistoricoInvalido(
                f"Histórico tem {len(historico)} entradas, "
                f"mas foi pedido índice {n}"
            )
        return historico[n]
 
    # (NUM MEM) — escrita em memória
    if (len(interior) == 2 and
            tipo(interior[0]) == T_NUM and
            tipo(interior[1]) == T_MEM):
        v    = float(valor(interior[0]))
        nome = valor(interior[1])
        memoria[nome] = v
        return v
 
    # Aritmética RPN com pilha
    pilha = []
 
    for tok in interior:
        t = tipo(tok)
        v = valor(tok)
 
        if t == T_NUM:
            pilha.append(float(v))
 
        elif t == T_OP:
            if len(pilha) < 2:
                raise ErroExpressaoInvalida(
                    f"Operador '{v}' requer 2 operandos, "
                    f"pilha tem {len(pilha)}"
                )
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(_aplicar_operador(v, a, b))
 
        elif t == T_MEM:
            nome = v
            if nome not in memoria:
                raise ErroMemoriaNaoInicializada(
                    f"Memória '{nome}' usada antes de ser inicializada"
                )
            pilha.append(memoria[nome])
 
        elif t == T_RES:
            raise ErroExpressaoInvalida(
                "RES deve ser precedido de um número inteiro: (N RES)"
            )
 
        else:
            raise ErroExpressaoInvalida(f"Token inesperado na avaliação: {tok}")
 
    if len(pilha) != 1:
        raise ErroExpressaoInvalida(
            f"Expressão RPN malformada: pilha tem {len(pilha)} "
            f"elemento(s) ao final (esperado 1)"
        )
 
    return pilha[0]

# Pré-processador de aninhamento
 
def preprocessar_aninhamento(tokens: list, memoria: dict, historico: list) -> list:
    """
    Resolve expressões aninhadas de dentro para fora. Cada iteração:
 
    - Lê a lista completa de tokens da esquerda para a direita
    - Ao encontrar um LPAREN cujo interior não tem outros LPAREN, identifica
      como o mais interno, avalia com a pilha e substitui o segmento pelo
      valor calculado como token NUM
    - Reinicia a varredura
    - Para quando o único LPAREN restante é o da expressão externa
    """
    while True:
        encontrou = False
 
        for i in range(len(tokens)):
            if tipo(tokens[i]) != T_LPAREN:
                continue
 
            fechamento = encontrar_fechamento(tokens, i)
            interior   = tokens[i + 1 : fechamento]
 
            tem_aninhado = any(tipo(t) == T_LPAREN for t in interior)
            if tem_aninhado:
                continue
 
            externos = [
                t for t in (tokens[:i] + tokens[fechamento + 1:])
                if tipo(t) == T_LPAREN
            ]
            if not externos:
                break
 
            sub_tokens = tokens[i : fechamento + 1]
            resultado = _avaliar_expressao_plana(sub_tokens, memoria, historico)
            token_resultado = (T_NUM, repr(resultado), 0)
            tokens = tokens[:i] + [token_resultado] + tokens[fechamento + 1:]
            encontrou = True
            break
 
        if not encontrou:
            break
 
    return tokens
 
def executarExpressao(tokens: list, memoria: dict, historico: list) -> float:
    """
    Avalia uma expressão RPN representada como lista de tuplas.
 
    Passos:
        1. Pré-processa expressões aninhadas (preprocessar_aninhamento)
        2. Avalia a expressão plana resultante com pilha (IEEE 754 64 bits)
        3. Insere o resultado no início do histórico
 
    Parâmetros:
        tokens   : list[tuple] — saída de parseExpressao
        memoria  : dict        — { "NOME": float } compartilhado entre linhas
        historico: list[float] — índice 0 = resultado mais recente
 
    Retorno:
        float — resultado da expressão
 
    Lança:
        LexError                   — token inválido (do lexer)
        ErroExpressaoInvalida      — estrutura RPN inválida
        ErroDivisaoPorZero         — divisão por zero
        ErroMemoriaNaoInicializada — MEM não inicializado
        ErroHistoricoInvalido      — (N RES) fora do intervalo
    """
    tokens_planos = preprocessar_aninhamento(
        list(tokens),
        memoria,
        historico
    )
 
    resultado = _avaliar_expressao_plana(tokens_planos, memoria, historico)
 
    historico.insert(0, resultado)
 
    return resultado
