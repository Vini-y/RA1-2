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

def _cabecalho(data):
    linhas = [".cpu cortex-a9", ".fpu vfpv3-d16", ".global _start", ".data"]
    linhas.extend(data)
    linhas += ["", ".text", "_start:"]
    linhas += ["    @ Habilitar VFP",
               "    VMRS r0, FPEXC",
               "    ORR  r0, r0, #0x40000000",
               "    VMSR FPEXC, r0", ""]
    return linhas

def _rodape():
    return ["", "_end:", "    B _end"]


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
    code.append("    @ OP //")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VDIV.F64 d2, d0, d1")
    code.append("    VCVT.S32.F64 s4, d2")
    code.append("    VCVT.F64.S32 d2, s4")
    code.append("    VPUSH {d2}")

def _op_mod(code):
    code.append("    @ OP %")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VDIV.F64 d2, d0, d1")
    code.append("    VCVT.S32.F64 s4, d2")
    code.append("    VCVT.F64.S32 d2, s4")
    code.append("    VMUL.F64 d2, d2, d1")
    code.append("    VSUB.F64 d2, d0, d2")
    code.append("    VPUSH {d2}")

_pow_count = 0

def _op_pow(code):
    global _pow_count
    loop_label = f"pow_loop_{_pow_count}"
    done_label = f"pow_done_{_pow_count}"
    _pow_count += 1
    code.append("    @ OP ^")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VCVT.S32.F64 s2, d1")
    code.append("    VMOV  r0, s2")
    code.append("    VMOV.F64 d2, d0")
    code.append("    SUBS  r0, r0, #1")
    code.append(f"    BEQ   {done_label}")
    code.append(f"{loop_label}:")
    code.append("    VMUL.F64 d2, d2, d0")
    code.append("    SUBS  r0, r0, #1")
    code.append(f"    BNE   {loop_label}")
    code.append(f"{done_label}:")
    code.append("    VPUSH {d2}")

def _emit_num(code, valor, label):
    code.append(f"    @ Carregar {valor}")
    code.append(f"    LDR  r0, ={label}")
    code.append(f"    VLDR d0, [r0]")
    code.append(f"    VPUSH {{d0}}")

def _mem_store(code, nome, label):
    code.append(f"    @ Armazenar em {nome}")
    code.append(f"    VPOP  {{d0}}")
    code.append(f"    LDR   r1, ={label}")
    code.append(f"    VSTR  d0, [r1]")

def _mem_load(code, nome, label):
    code.append(f"    @ Carregar {nome}")
    code.append(f"    LDR   r1, ={label}")
    code.append(f"    VLDR  d0, [r1]")
    code.append(f"    VPUSH {{d0}}")

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
    sig = [(t, v) for t, v, _ in tokens if t not in ("LPAREN", "RPAREN")]
    return len(sig) == 2 and sig[0][0] in ("INT", "FLOAT") and sig[1][0] == "MEM"

def _div10(code):
    code.append(f"    UMULL r0, r1, r4, r9")
    code.append(f"    LSR   r1, r1, #3")
    code.append(f"    MOV   r0, #10")
    code.append(f"    MUL   r2, r1, r0")
    code.append(f"    SUB   r2, r4, r2")
    code.append(f"    MOV   r4, r1")

def _exibir_resultado(code, L):
    code.append(f"    @ Exibir resultado no HEX")
    code.append(f"    VCVT.S32.F64 s0, d0")
    code.append(f"    VMOV  r4, s0")
    code.append(f"    MOV   r8, #0")
    code.append(f"    CMP   r4, #0")
    code.append(f"    BGE   _dp_{L}")
    code.append(f"    MOV   r8, #0x40")
    code.append(f"    RSB   r4, r4, #0")
    code.append(f"_dp_{L}:")
    code.append(f"    LDR   r6, =_seg7")
    code.append(f"    LDR   r9, =0xCCCCCCCD")
    _div10(code)
    code.append(f"    LDRB  r5, [r6, r2]")
    for shift in [8, 16, 24]:
        _div10(code)
        code.append(f"    LDRB  r3, [r6, r2]")
        code.append(f"    ORR   r5, r5, r3, LSL #{shift}")
    code.append(f"    LDR   r0, =0xFF200020")
    code.append(f"    STR   r5, [r0]")
    _div10(code)
    code.append(f"    LDRB  r7, [r6, r2]")
    _div10(code)
    code.append(f"    LDRB  r3, [r6, r2]")
    code.append(f"    CMP   r4, #0")
    code.append(f"    MOVEQ r3, r8")
    code.append(f"    ORR   r7, r7, r3, LSL #8")
    code.append(f"    LDR   r0, =0xFF200030")
    code.append(f"    STR   r7, [r0]")
    code.append(f"    BKPT  #0")

def gerarAssembly(tokens_por_linha):
    data, code  = [], []
    num_labels  = {}
    mem_labels  = {}
    res_labels  = []
    label_count = 0

    data += [f"{INDENT}_seg7: .byte 0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F"]

    for L in range(len(tokens_por_linha)):
        label = f"result_{L}"
        res_labels.append(label)
        data += [f"{INDENT}.align 3", f"{INDENT}{label}: .double 0.0"]

    for L, tokens in enumerate(tokens_por_linha):
        for i, (tipo, valor, _) in enumerate(tokens):
            if tipo in ("INT", "FLOAT"):
                prox = tokens[i + 1][0] if i + 1 < len(tokens) else None
                if prox == "RES":
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

    for L, tokens in enumerate(tokens_por_linha):
        prev_tipo = None
        res_n     = None

        for i, (tipo, valor, _) in enumerate(tokens):
            if tipo in ("INT", "FLOAT"):
                prox = tokens[i + 1][0] if i + 1 < len(tokens) else None
                if prox == "RES":
                    res_n = valor
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
                if prev_tipo == "NUM" and prox_tipo == "RPAREN":
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

        if _is_store(tokens):
            code.append(f"    LDR   r1, ={res_labels[L]}")
            code.append(f"    VSTR  d0, [r1]")
        else:
            code.append(f"    VPOP  {{d0}}")
            code.append(f"    LDR   r1, ={res_labels[L]}")
            code.append(f"    VSTR  d0, [r1]")
        _exibir_resultado(code, L)

    return "\n".join(_cabecalho(data) + code + _rodape())