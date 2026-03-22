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
    linhas = [".global _start", ".data"]
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
    code.append("    VCVT.S32.F64 s0, d0")
    code.append("    VCVT.S32.F64 s2, d1")
    code.append("    VMOV r0, s0")
    code.append("    VMOV r1, s2")
    code.append("    SDIV r2, r0, r1")
    code.append("    VMOV s4, r2")
    code.append("    VCVT.F64.S32 d2, s4")
    code.append("    VPUSH {d2}")

def _op_mod(code):
    code.append("    @ OP %")
    code.append("    VPOP  {d1}")
    code.append("    VPOP  {d0}")
    code.append("    VCVT.S32.F64 s0, d0")
    code.append("    VCVT.S32.F64 s2, d1")
    code.append("    VMOV r0, s0")
    code.append("    VMOV r1, s2")
    code.append("    SDIV r2, r0, r1")
    code.append("    MUL  r3, r2, r1")
    code.append("    SUB  r2, r0, r3")
    code.append("    VMOV s4, r2")
    code.append("    VCVT.F64.S32 d2, s4")
    code.append("    VPUSH {d2}")

def _emit_num(code, valor, label):
    code.append(f"    @ Carregar {valor}")
    code.append(f"    LDR  r0, ={label}")
    code.append(f"    VLDR d0, [r0]")
    code.append(f"    VPUSH {{d0}}")

OP_HANDLERS = {
    "+": _op_add,
    "-": _op_sub,
    "*": _op_mul,
    "/": _op_div,
    "//": _op_floordiv,
    "%": _op_mod,
}

INDENT = "    "

def gerarAssembly(tokens):
    data, code = [], []
    num_labels = {}
    label_count = 0

    for i, (tipo, valor, _) in enumerate(tokens):
        if tipo == "NUM":
            label = f"val_{label_count}"
            num_labels[i] = label
            data += [f"{INDENT}.align 3", f"{INDENT}{label}: .double {valor}"]
            label_count += 1

    for i, (tipo, valor, _) in enumerate(tokens):
        if tipo == "NUM":
            _emit_num(code, valor, num_labels[i])
        elif tipo == "OP":
            if valor in OP_HANDLERS:
                OP_HANDLERS[valor](code)

    return "\n".join(_cabecalho(data) + code + _rodape())