# Grupo no Canvas: RA1 2

# Integrantes (ordem alfabética) e GitHub:
# - Gabriel Vidal Schneider (@Gabiru1089)
# - Lucca Fabricio Magalhães (@luccafm1)
# - Mohamad Kassem Diab (@Mo1409)
# - Vinícius Yamamoto Borges (@Vini-y)


from lexer import parseExpressao, LexError

"""
executarExpressao.py

Avalia as expressões produzidas em lexer.py

Formato do Token esperado: tupla (tipo, valor, posição)
    ("INT",   "10",   1)
    ("FLOAT", "3.14", 1)
    ("OP", "+", 7)
    ("LPAREN", "(", 0)
    ("RPAREN", ")", 9)
    ("RES", "RES", 5)
    ("MEM", "VAR", 3)

Depende de:
    lexer.py -> parseExpressao

"""

# Constantes - tipos de token do lexer
T_FLOAT ="FLOAT"
T_INT = "INT"
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

def eh_numero(token: tuple) -> bool:
    """Retorna True se o token é um número (INT ou FLOAT)."""
    return tipo(token) in (T_INT, T_FLOAT)

# Exceções específicas de execução

class ErroDivisaoPorZero(Exception):
    pass

class ErroExpressaoInvalida(Exception):
    pass

class ErroMemoriaNaoInicializada(Exception):
    pass
class ErroHistoricoInvalido(Exception):
    pass

# Encontra o fechamento de um LPAREN específico (RPAREN equivalente)
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

    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
 
    if op == '/':
        if b == 0.0:
            raise ErroDivisaoPorZero(f"Divisão real por zero: {a} / {b}")
        return a / b
 
    if op == '//':
        if b == 0:
            raise ErroDivisaoPorZero(f"Divisão inteira por zero: {a} // {b}")
        # int() garante semântica de inteiro, float() mantém pilha uniforme
        return float(int(a) // int(b))
 
    if op == '%':
        if b == 0:
            raise ErroDivisaoPorZero(f"Resto por zero: {a} % {b}")
        return float(int(a) % int(b))
 
    if op == '^':
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
      ( MEM )             -> leitura de variável de memória
      ( INT|FLOAT RES )   -> retorna resultado N linhas anteriores
      ( INT|FLOAT MEM )   -> escrita em variável de memória
      ( INT|FLOAT... OP ) -> aritmética RPN com pilha
    """
    # Remove parênteses externos para trabalhar com o interior
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
 
    # (INT|FLOAT RES) — N linhas anteriores
    # N=1 - linha imediatamente anterior - historico[0]
    # N=2 - duas linhas atrás - historico[1]
    # índice no histórico = n - 1
    if (len(interior) == 2 and
            eh_numero(interior[0]) and
            tipo(interior[1]) == T_RES):
        n = int(float(valor(interior[0])))
        if n <= 0:
            raise ErroHistoricoInvalido(
                f"N em (N RES) deve ser positivo, recebeu: {n}"
            )
        idx = n - 1
        if idx >= len(historico):
            raise ErroHistoricoInvalido(
                f"Histórico tem {len(historico)} entradas, "
                f"mas foi pedido {n} linhas atrás (índice {idx})"
            )
        return historico[idx]
 
    # (INT|FLOAT MEM) — escrita em variável
    if (len(interior) == 2 and
            eh_numero(interior[0]) and
            tipo(interior[1]) == T_MEM):
        v    = float(valor(interior[0]))
        nome = valor(interior[1])
        memoria[nome] = v
        return v
 
    # Aritmética RPN com pilha
    # Para cada token do interior:
    # INT ou FLOAT - converte para float e empilha
    # OP - desempilha b e a, aplica operador, empilha resultado
    # MEM - lê variável da memória e empilha
    pilha = []
 
    for tok in interior:
        t = tipo(tok)
        v = valor(tok)
 
        # INT e FLOAT são ambos empilhados como float
        if t in (T_INT, T_FLOAT):
            pilha.append(float(v))
 
        elif t == T_OP:
            if len(pilha) < 2:
                raise ErroExpressaoInvalida(
                    f"Operador '{v}' requer 2 operandos, "
                    f"pilha tem {len(pilha)}"
                )
            # Em RPN: topo da pilha é b, segundo elemento é a - (a b op)
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(_aplicar_operador(v, a, b))
 
        elif t == T_MEM:
            # MEM usada como operando em expressão aritmética
            nome = v
            if nome not in memoria:
                raise ErroMemoriaNaoInicializada(
                    f"Memória '{nome}' usada antes de ser inicializada"
                )
            pilha.append(memoria[nome])
 
        elif t == T_RES:
            # RES sem número antes é erro de estrutura
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
 
    - Varre a lista da esquerda para a direita
    - Ao encontrar um LPAREN cujo interior não tem outros LPAREN,
      identifica como o mais interno e avalia com _avaliar_expressao_plana
    - Substitui o segmento inteiro pelo resultado como token INT
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
 
            # Se o interior tem outro LPAREN, ainda há aninhamento — pula
            tem_aninhado = any(tipo(t) == T_LPAREN for t in interior)
            if tem_aninhado:
                continue
 
            # Se não há LPAREN fora deste segmento, é a expressão final
            externos = [
                t for t in (tokens[:i] + tokens[fechamento + 1:])
                if tipo(t) == T_LPAREN
            ]
            if not externos:
                break
 
            # Avalia a sub-expressão mais interna e substitui pelo resultado
            sub_tokens      = tokens[i : fechamento + 1]
            resultado       = _avaliar_expressao_plana(sub_tokens, memoria, historico)
 
            # Usa INT como tipo do token resultado (posição 0 como placeholder)
            token_resultado = (T_INT, repr(resultado), 0)
            tokens          = tokens[:i] + [token_resultado] + tokens[fechamento + 1:]
            encontrou       = True
            break
 
        if not encontrou:
            break
 
    return tokens
 
 
def executarExpressao(tokens: list, memoria: dict, historico: list) -> float:
    """
    Avalia uma expressão RPN representada como lista de tuplas.
 
    Passos:
        - Pré-processa expressões aninhadas (preprocessar_aninhamento)
        - Avalia a expressão plana resultante com pilha (IEEE 754 64 bits)
        - Insere o resultado no início do histórico
 
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


def testeExecutar():
    histTest = []
    memTest = {}
    stringTeste = ["(2 2 +)", "(100 SOMA)", "(6 7 *)", "(1 RES)", "((2 2 +) 4 *)", "(5 4 /)",
                   "(8 3 //)", "(8 3 %)", "(2 3 ^)"]
    
    for i in range(len(stringTeste)):
        tokens = []
        parseExpressao(stringTeste[i], tokens)
        resultado = executarExpressao(tokens, memTest, histTest)
        print(f"Resultado{i}: {resultado}")
    print(f"Histórico: {histTest}")
    print(f"Memoria: {memTest}")

if __name__ == "__main__":
    testeExecutar()
