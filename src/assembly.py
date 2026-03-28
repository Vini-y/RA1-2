# Grupo no Canvas: RA1 2

# Integrantes (ordem alfabética) e GitHub:
# - Gabriel Vidal Schneider (@Gabiru1089)
# - Lucca Fabricio Magalhães (@luccafm1)
# - Mohamad Kassem Diab (@Mo1409)
# - Vinícius Yamamoto Borges (@Vini-y)

# Leitura de arquivo e gerador de Assembly ARMv7
# Recebe o vetor de tokens do analisador léxico e traduz
# para Assembly compatível com CPUlator DEC1-SOC (v16.1).
# Todos os valores são armazenados como .double (IEEE 754 64 bits).

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


# --- Cabeçalho e rodapé do Assembly ---

def _cabecalho(data):
    """Gera as diretivas iniciais (.cpu, .fpu, .data) e habilita o VFP."""
    linhas = [".cpu cortex-a9", ".fpu vfpv3-d16", ".global _start", ".data"]
    linhas.extend(data)
    linhas += ["", ".text", "_start:"]
    linhas += ["    @ Habilitar VFP",
               "    VMRS r0, FPEXC",
               "    ORR  r0, r0, #0x40000000",
               "    VMSR FPEXC, r0", ""]
    return linhas

def _rodape():
    """Loop infinito no final para manter o programa parado no CPUlator."""
    return ["", "_end:", "    B _end"]


# --- Emissão de instruções para cada operação aritmética ---
# Todas desempilham dois operandos (d0, d1), operam, e empilham o resultado.
# Usam VFP double precision (F64) conforme exigido pelo trabalho.

def _op_add(code):
    code.append("    @ OP +")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VADD.F64 d2, d0, d1")
    code.append("    VPUSH {d2}")

def _op_sub(code):
    code.append("    @ OP -")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VSUB.F64 d2, d0, d1")
    code.append("    VPUSH {d2}")

def _op_mul(code):
    code.append("    @ OP *")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VMUL.F64 d2, d0, d1")
    code.append("    VPUSH {d2}")

def _op_div(code):
    code.append("    @ OP /")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VDIV.F64 d2, d0, d1")
    code.append("    VPUSH {d2}")

def _op_floordiv(code):
    """Divisão inteira: divide, trunca para inteiro e converte de volta para double."""
    code.append("    @ OP //")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VDIV.F64 d2, d0, d1")
    code.append("    VCVT.S32.F64 s4, d2")
    code.append("    VCVT.F64.S32 d2, s4")
    code.append("    VPUSH {d2}")

def _op_mod(code):
    """Resto: calcula d0 - (truncado(d0/d1) * d1)."""
    code.append("    @ OP %")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VDIV.F64 d2, d0, d1")
    code.append("    VCVT.S32.F64 s4, d2")
    code.append("    VCVT.F64.S32 d2, s4")
    code.append("    VMUL.F64 d2, d2, d1")
    code.append("    VSUB.F64 d2, d0, d2")
    code.append("    VPUSH {d2}")

# Contador global para gerar labels únicos de potência (pow_loop_0, pow_loop_1, ...)
_pow_count = 0

def _op_pow(code):
    """Potência por multiplicação repetida (expoente inteiro positivo)."""
    global _pow_count
    loop_label = f"pow_loop_{_pow_count}"
    done_label = f"pow_done_{_pow_count}"
    _pow_count += 1
    code.append("    @ OP ^")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VCVT.S32.F64 s2, d1")   # expoente para inteiro
    code.append("    VMOV  r0, s2")
    code.append("    VMOV.F64 d2, d0")        # d2 = base (acumulador)
    code.append("    SUBS  r0, r0, #1")
    code.append(f"    BEQ   {done_label}")    # expoente 1 -> já tem o resultado
    code.append(f"{loop_label}:")
    code.append("    VMUL.F64 d2, d2, d0")
    code.append("    SUBS  r0, r0, #1")
    code.append(f"    BNE   {loop_label}")
    code.append(f"{done_label}:")
    code.append("    VPUSH {d2}")


# --- Emissão de instruções auxiliares ---

def _emit_num(code, valor, label):
    """Carrega uma constante numérica da seção .data e empilha."""
    code.append(f"    @ Carregar {valor}")
    code.append(f"    LDR  r0, ={label}")
    code.append(f"    VLDR d0, [r0]")
    code.append(f"    VPUSH {{d0}}")

def _mem_store(code, nome, label):
    """Desempilha d0 e armazena na variável MEM."""
    code.append(f"    @ Armazenar em {nome}")
    code.append(f"    VPOP  {{d0}}")
    code.append(f"    LDR   r1, ={label}")
    code.append(f"    VSTR  d0, [r1]")

def _mem_load(code, nome, label):
    """Carrega o valor da variável MEM e empilha."""
    code.append(f"    @ Carregar {nome}")
    code.append(f"    LDR   r1, ={label}")
    code.append(f"    VLDR  d0, [r1]")
    code.append(f"    VPUSH {{d0}}")

# Mapa de operadores para suas funções de emissão
OP_HANDLERS = {
    "+": _op_add,
    "-": _op_sub,
    "*": _op_mul,
    "/": _op_div,
    "//": _op_floordiv,
    "%": _op_mod,
    "^": _op_pow,
}

INDENT = "    "

def _is_store(tokens):
    """Detecta se a expressão é um store em memória: (V MEM)."""
    sig = [(t, v) for t, v, _ in tokens if t not in ("LPAREN", "RPAREN")]
    return len(sig) == 2 and sig[0][0] in ("INT", "FLOAT") and sig[1][0] == "MEM"


# --- Exibição de resultado via JTAG UART ---

def _exibir_resultado(code, L):
    """
    Imprime o valor de d0 no JTAG UART com 1 casa decimal.
    Salva d0 em d3 (pois VCVT corrompe s0/s1 que compõem d0).
    Usa s4 (parte de d2) e s8 (parte de d4) para conversões intermediárias.
    Fluxo: sinal -> parte inteira (dígitos via pilha) -> '.' -> 1 dígito decimal -> '\\n'
    """
    code.append(f"    @ Exibir resultado via JTAG UART (1 casa decimal)")
    code.append(f"    VMOV.F64 d3, d0")            # salva valor original
    code.append(f"    LDR   r5, =0xFF201000")       # endereço JTAG UART

    # Verifica sinal: se negativo, imprime '-' e nega
    code.append(f"    VCMP.F64 d3, #0")
    code.append(f"    VMRS  APSR_nzcv, FPSCR")
    code.append(f"    BGE   _uart_pos_{L}")
    code.append(f"    MOV   r0, #0x2D")
    code.append(f"    STR   r0, [r5]")
    code.append(f"    VNEG.F64 d3, d3")

    # Extrai parte inteira em r4
    code.append(f"_uart_pos_{L}:")
    code.append(f"    VCVT.S32.F64 s4, d3")         # s4 = int(d3)
    code.append(f"    VMOV  r4, s4")

    # Caso especial: parte inteira é zero
    code.append(f"    CMP   r4, #0")
    code.append(f"    BNE   _uart_conv_{L}")
    code.append(f"    MOV   r0, #0x30")
    code.append(f"    STR   r0, [r5]")
    code.append(f"    B     _uart_dot_{L}")

    # Extrai dígitos da parte inteira (divisão por 10 via UMULL)
    # Os dígitos saem em ordem inversa, então empilha e depois desempilha
    code.append(f"_uart_conv_{L}:")
    code.append(f"    MOV   r6, #0")                 # contador de dígitos
    code.append(f"    LDR   r9, =0xCCCCCCCD")        # constante mágica para div por 10
    code.append(f"_uart_loop_{L}:")
    code.append(f"    CMP   r4, #0")
    code.append(f"    BEQ   _uart_print_{L}")
    code.append(f"    UMULL r0, r1, r4, r9")         # r1 = (r4 * magic) >> 32
    code.append(f"    LSR   r1, r1, #3")             # r1 = quociente (r4 / 10)
    code.append(f"    MOV   r0, #10")
    code.append(f"    MUL   r2, r1, r0")
    code.append(f"    SUB   r2, r4, r2")             # r2 = resto (dígito)
    code.append(f"    MOV   r4, r1")
    code.append(f"    ADD   r2, r2, #0x30")          # converte para ASCII
    code.append(f"    PUSH  {{r2}}")
    code.append(f"    ADD   r6, r6, #1")
    code.append(f"    B     _uart_loop_{L}")

    # Desempilha e imprime dígitos na ordem correta
    code.append(f"_uart_print_{L}:")
    code.append(f"    CMP   r6, #0")
    code.append(f"    BEQ   _uart_dot_{L}")
    code.append(f"    POP   {{r0}}")
    code.append(f"    STR   r0, [r5]")
    code.append(f"    SUB   r6, r6, #1")
    code.append(f"    B     _uart_print_{L}")

    # Imprime '.' e calcula 1 dígito decimal: int(frac * 10)
    code.append(f"_uart_dot_{L}:")
    code.append(f"    MOV   r0, #0x2E")
    code.append(f"    STR   r0, [r5]")
    code.append(f"    VCVT.F64.S32 d1, s4")          # d1 = float(parte inteira)
    code.append(f"    VSUB.F64 d1, d3, d1")          # d1 = parte fracionária
    code.append(f"    MOV   r0, #10")
    code.append(f"    VMOV  s8, r0")
    code.append(f"    VCVT.F64.S32 d4, s8")          # d4 = 10.0
    code.append(f"    VMUL.F64 d1, d1, d4")          # d1 = frac * 10
    code.append(f"    VCVT.S32.F64 s4, d1")          # s4 = dígito decimal
    code.append(f"    VMOV  r0, s4")
    code.append(f"    ADD   r0, r0, #0x30")
    code.append(f"    STR   r0, [r5]")

    # Newline
    code.append(f"    MOV   r0, #0x0A")
    code.append(f"    STR   r0, [r5]")


# --- Função principal de geração ---

def gerarAssembly(tokens_por_linha):
    """
    Recebe uma lista de listas de tokens (uma por linha do arquivo fonte)
    e retorna uma string com o código Assembly ARMv7 completo.

    Etapas:
    1. Aloca labels .double na seção .data para resultados, constantes e variáveis
    2. Percorre os tokens e emite instruções VFP para cada operação
    3. Após cada linha, salva o resultado e exibe via JTAG UART
    """
    data, code  = [], []
    num_labels  = {}     # (linha, indice) -> label da constante
    mem_labels  = {}     # nome_variavel -> label da variável
    res_labels  = []     # label do resultado de cada linha
    label_count = 0

    # Aloca espaço para o resultado de cada linha
    for L in range(len(tokens_por_linha)):
        label = f"result_{L}"
        res_labels.append(label)
        data += [f"{INDENT}.align 3", f"{INDENT}{label}: .double 0.0"]

    # Primeira passada: coleta constantes e variáveis para a seção .data
    for L, tokens in enumerate(tokens_por_linha):
        for i, (tipo, valor, _) in enumerate(tokens):
            if tipo in ("INT", "FLOAT"):
                prox = tokens[i + 1][0] if i + 1 < len(tokens) else None
                if prox == "RES":
                    # número antes de RES é o N, não precisa de label
                    num_labels[(L, i)] = None
                else:
                    label = f"val_{label_count}"
                    num_labels[(L, i)] = label
                    data += [f"{INDENT}.align 3", f"{INDENT}{label}: .double {valor}"]
                    label_count += 1
            elif tipo == "MEM":
                if valor not in mem_labels:
                    label = f"var_{valor}"
                    mem_labels[valor] = label
                    data += [f"{INDENT}.align 3", f"{INDENT}{label}: .double 0.0"]

    # Segunda passada: emite instruções para cada token
    for L, tokens in enumerate(tokens_por_linha):
        prev_tipo = None
        res_n     = None

        for i, (tipo, valor, _) in enumerate(tokens):
            if tipo in ("INT", "FLOAT"):
                prox = tokens[i + 1][0] if i + 1 < len(tokens) else None
                if prox == "RES":
                    res_n = valor  # guarda N para usar no token RES
                else:
                    _emit_num(code, valor, num_labels[(L, i)])
                    prev_tipo = tipo
            elif tipo == "OP":
                if valor in OP_HANDLERS:
                    OP_HANDLERS[valor](code)
                prev_tipo = tipo
            elif tipo == "MEM":
                label     = mem_labels[valor]
                prox_tipo = tokens[i + 1][0] if i + 1 < len(tokens) else None
                # (V MEM) -> store, senão -> load
                if prev_tipo in ("INT", "FLOAT") and prox_tipo == "RPAREN":
                    _mem_store(code, valor, label)
                else:
                    _mem_load(code, valor, label)
                prev_tipo = tipo
            elif tipo == "RES":
                target = L - int(res_n)
                code.append(f"    @ ({res_n} RES)")
                code.append(f"    LDR   r1, ={res_labels[target]}")
                code.append(f"    VLDR  d0, [r1]")
                code.append(f"    VPUSH {{d0}}")
                res_n     = None
                prev_tipo = tipo

        # Salva resultado da linha e exibe no UART
        if _is_store(tokens):
            code.append(f"    LDR   r1, ={res_labels[L]}")
            code.append(f"    VSTR  d0, [r1]")
        else:
            code.append(f"    VPOP  {{d0}}")
            code.append(f"    LDR   r1, ={res_labels[L]}")
            code.append(f"    VSTR  d0, [r1]")
        _exibir_resultado(code, L)

    return "\n".join(_cabecalho(data) + code + _rodape())


# --- Funções de teste ---

import tempfile, os

def _tok(linha_str):
    """Tokeniza uma linha usando o lexer para gerar tokens de teste."""
    from lexer import parseExpressao
    tokens = []
    parseExpressao(linha_str, tokens)
    return tokens


def teste_lerArquivo_valido():
    """Testa leitura de um arquivo válido com múltiplas linhas."""
    conteudo = "(3.14 2.0 +)\n(10 5 -)\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                      delete=False, encoding="utf-8") as f:
        f.write(conteudo)
        caminho = f.name

    backup = sys.argv[:]
    sys.argv = ["assembly.py", caminho]
    try:
        linhas = lerArquivo()
        assert len(linhas) == 2, f"Esperado 2 linhas, obteve {len(linhas)}"
        assert linhas[0] == "(3.14 2.0 +)", f"Linha 0 inesperada: {linhas[0]}"
        assert linhas[1] == "(10 5 -)", f"Linha 1 inesperada: {linhas[1]}"
        print("[PASS] teste_lerArquivo_valido")
    finally:
        sys.argv = backup
        os.unlink(caminho)


def teste_lerArquivo_arquivo_vazio():
    """Testa leitura de um arquivo vazio."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                      delete=False, encoding="utf-8") as f:
        caminho = f.name

    backup = sys.argv[:]
    sys.argv = ["assembly.py", caminho]
    try:
        linhas = lerArquivo()
        assert linhas == [], f"Esperado lista vazia, obteve {linhas}"
        print("[PASS] teste_lerArquivo_arquivo_vazio")
    finally:
        sys.argv = backup
        os.unlink(caminho)


def teste_assembly_todas_operacoes():
    """
    Verifica que o assembly gerado a partir de um arquivo de teste
    contém todas as operações exigidas: +, -, *, /, //, %, ^
    e os comandos especiais: (V MEM), (MEM), (N RES).
    Também valida a estrutura (cabeçalho, rodapé, UART, IEEE 754).
    """
    linhas_teste = [
        "(5.5 1.5 +)",
        "(12 7 -)",
        "(3.5 6.0 *)",
        "(18.0 5.0 /)",
        "(25 4 //)",
        "(25 4 %)",
        "(3.0 5 ^)",
        "(42.0 TOTAL)",
        "(TOTAL)",
        "(1 RES)",
        "((2.5 3.0 *) (5.0 2.0 +) /)",
    ]
    tokens_por_linha = [_tok(l) for l in linhas_teste]
    asm = gerarAssembly(tokens_por_linha)

    # cabeçalho ARMv7
    assert ".cpu cortex-a9" in asm, "Faltando .cpu"
    assert ".fpu vfpv3-d16" in asm, "Faltando .fpu"
    assert ".global _start" in asm, "Faltando .global _start"
    assert "VMRS r0, FPEXC" in asm, "Faltando habilitação do VFP"

    # rodapé
    assert "_end:" in asm, "Faltando label _end"
    assert "B _end" in asm, "Faltando loop infinito no rodapé"

    # todas as operações aritméticas
    assert "VADD.F64" in asm, "Faltando operação de adição (+)"
    assert "VSUB.F64" in asm, "Faltando operação de subtração (-)"
    assert "VMUL.F64" in asm, "Faltando operação de multiplicação (*)"
    assert "VDIV.F64" in asm, "Faltando operação de divisão (/)"
    assert "pow_loop_" in asm, "Faltando operação de potência (^)"

    # divisão inteira (//) — trunca para inteiro e volta para double
    assert "@ OP //" in asm, "Faltando comentário de divisão inteira"

    # resto (%) — subtrai quociente truncado * divisor
    assert "@ OP %" in asm, "Faltando comentário de resto"

    # (V MEM) — armazenamento em variável
    assert "var_TOTAL: .double 0.0" in asm, "Faltando alocação da variável TOTAL"
    assert "Armazenar em TOTAL" in asm, "Faltando store em TOTAL"

    # (MEM) — leitura de variável
    assert "Carregar TOTAL" in asm, "Faltando load de TOTAL"

    # (N RES) — referência a resultado anterior
    assert "(1 RES)" in asm, "Faltando comentário de RES"
    assert "result_0" in asm, "Faltando referência a resultado anterior"

    # constantes com inteiros e reais (IEEE 754 64 bits)
    assert ".double 5.5" in asm, "Faltando constante real 5.5"
    assert ".double 12" in asm, "Faltando constante inteira 12"
    assert ".float" not in asm, "Não deve usar .float (32 bits)"

    # saída via JTAG UART
    assert "0xFF201000" in asm, "Faltando endereço JTAG UART"
    assert "0x2E" in asm, "Faltando impressão do ponto decimal"
    assert "0x0A" in asm, "Faltando impressão do newline"

    print("[PASS] teste_assembly_todas_operacoes")


if __name__ == "__main__":
    testes = [
        teste_lerArquivo_valido,
        teste_lerArquivo_arquivo_vazio,
        teste_assembly_todas_operacoes,
    ]

    falhas = 0
    for teste in testes:
        _pow_count = 0
        try:
            teste()
        except AssertionError as e:
            print(f"[FAIL] {teste.__name__}: {e}")
            falhas += 1
        except Exception as e:
            print(f"[ERRO] {teste.__name__}: {type(e).__name__}: {e}")
            falhas += 1

    print(f"\n{len(testes) - falhas}/{len(testes)} testes passaram.")
    if falhas:
        sys.exit(1)
