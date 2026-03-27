# Grupo no Canvas: RA1 2

# Integrantes (ordem alfabética) e GitHub:
# - Gabriel Vidal Schneider (@Gabiru1089)
# - Lucca Fabricio Magalhães (@luccafm1)
# - Mohamad Kassem Diab (@Mo1409)
# - Vinícius Yamamoto Borges (@Vini-y)

from typing import Callable, Any
from string import ascii_uppercase

Token = tuple[str, str, int] 
Estado = tuple[Callable[..., Any] | None, int, list[Token], str]

class LexError (Exception):
    ...

_OP = r"+-*%^" # `/` não conta aqui, pois contamos `//` em um estado separado
_ABC= ascii_uppercase

def parseExpressao(linha: str, _tokens_: list[Token]) -> None:
    if not linha: return []
    
    length = len(linha)
    idx = 0
    word = "" #<- porque precisamos montar 'palavras', por exemplo um número de >1 digito

    read = estadoEntrada(linha, idx, _tokens_, word)
    while idx < length:
        state, idx, _tokens_, word = read
        read = state(linha, idx, _tokens_, word)

        if read is None:
            raise LexError(f'Token inválido ou malformado: {linha[idx]} na posição {idx}')

def estadoEntrada(linha: str, 
                  index: int, 
                  _tokens_: list[Token], 
                  word: str) -> Estado | None:
    
    if linha[index].isdecimal() : return estadoNumero,      index + 1, _tokens_, linha[index]
    if linha[index] in _OP      : return estadoOperador,    index + 1, _tokens_, linha[index]
    if linha[index] == '/'      : return estadoDivisao,     index + 1, _tokens_, linha[index]
    if linha[index] == '('      : return estadoLPAREN,      index + 1, _tokens_, linha[index]
    if linha[index] == ')'      : return estadoRPAREN,      index + 1, _tokens_, linha[index]
    if linha[index] == 'R'      : return estadoR,           index + 1, _tokens_, linha[index]
    if linha[index] in _ABC     : return estadoMEM,         index + 1, _tokens_, linha[index]
    if linha[index].isspace()   : return estadoWhiteSpace,  index + 1, _tokens_, linha[index]
    
    return None # <- token inválido

def estadoNumero(linha: str, 
                 index: int, 
                 _tokens_: list[Token], 
                 word: str) -> Estado | None:
    
    if index >= len(linha): 
        _tokens_.append(("INT", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index].isdecimal():
        return estadoNumero, index+1, _tokens_, word + linha[index]
    
    if linha[index] == '.':
        return estadoPonto, index+1, _tokens_, word + linha[index]

    _tokens_.append(("INT", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""

def estadoPonto(linha: str, 
                index: int, 
                _tokens_: list[Token], 
                word: str) -> Estado | None:
    
    if index >= len(linha):
        # número malformado: digito `n.` é inválido
        return None
    
    if linha[index].isdecimal():
        return estadoDecimal, index+1, _tokens_, word + linha[index]
    
    return None

def estadoDecimal(linha: str, 
                  index: int, 
                  _tokens_: list[Token], 
                  word: str) -> Estado | None:
    
    if index >= len(linha):
        _tokens_.append(("FLOAT", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index].isdecimal():
        return estadoDecimal, index+1, _tokens_, word + linha[index]
    
    if linha[index] == '.':
        # número malformado: mais de um ponto
        return None
    
    _tokens_.append(("FLOAT", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""


def estadoOperador(linha: str, 
                   index: int, 
                   _tokens_: list[Token], 
                   word: str) -> Estado | None:
    
    _tokens_.append(("OP", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""

def estadoDivisao(linha: str, 
                  index: int, 
                  _tokens_: list[Token], 
                  word: str) -> Estado | None:
    
    # note que todos os operadores são de apenas um caracter, exceto
    # divisão inteira (//)
    if index >= len(linha):
        _tokens_.append(("OP", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index] == '/':
        _tokens_.append(("OP", word + linha[index], index - len(word)))
        return estadoEntrada, index+1, _tokens_, ""
    
    _tokens_.append(("OP", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""
    
def estadoWhiteSpace(linha: str, 
                     index: int, 
                     _tokens_: list[Token], 
                     word: str) -> Estado | None:
    
    # não tokenizamos whitespace
    if index >= len(linha):
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index].isspace():
        return estadoWhiteSpace, index + 1, _tokens_, ""
    
    return estadoEntrada, index, _tokens_, ""

def estadoLPAREN(linha: str, 
                 index: int, 
                 _tokens_: list[Token], 
                 word: str) -> Estado | None:
    
    _tokens_.append(("LPAREN", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""
    
def estadoRPAREN(linha: str, 
                 index: int, 
                 _tokens_: list[Token], 
                 word: str) -> Estado | None:
    
    _tokens_.append(("RPAREN", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""

def estadoR(linha: str, 
            index: int, 
            _tokens_: list[Token], 
            word: str) -> Estado | None:
    
    if index >= len(linha):
        _tokens_.append(("MEM", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index] == 'E':
        return estadoE, index+1, _tokens_, word + linha[index]
    
    if linha[index] in _ABC:
        return estadoMEM, index + 1, _tokens_, word + linha[index]
    
    _tokens_.append(("MEM", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""
    

def estadoE(linha: str,
            index: int, 
            _tokens_: list[Token], 
            word: str) -> Estado | None:
    
    if index >= len(linha):
        _tokens_.append(("MEM", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""

    if linha[index] == 'S':
        return estadoS, index+1, _tokens_, word + linha[index]
    
    if linha[index] in _ABC:
        return estadoMEM, index + 1, _tokens_, word + linha[index]
    
    _tokens_.append(("MEM", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""
    
def estadoS(linha: str,
            index: int, 
            _tokens_: list[Token], 
            word: str) -> Estado | None:
    
    if index >= len(linha):
        _tokens_.append(("RES", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index] in _ABC:
        return estadoMEM, index+1, _tokens_, word + linha[index]
    
    _tokens_.append(("RES", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""

def estadoMEM(linha: str, 
              index: int, 
              _tokens_: list[Token], 
              word: str) -> Estado | None:
    
    if index >= len(linha):
        _tokens_.append(("MEM", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index] in _ABC:
        return estadoMEM, index+1, _tokens_, word + linha[index]
    
    _tokens_.append(("MEM", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""