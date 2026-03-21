# analisador léxico - aluno 1

from typing import List, Tuple
from string import ascii_uppercase

class LexError (Exception):
    ...

_OP = r"+-*%^" # `/` não conta aqui, pois contamos `//` em um estado separado
_ABC= ascii_uppercase

def parseExpressao(linha: str, _tokens_:List[Tuple[str, str, int]]) -> List[str]:
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
    
    _tokens_.sort(key=lambda f: f[2]) 

def estadoEntrada(linha: str, 
                  index: int = 0, 
                  _tokens_:List[Tuple[str, str, int]] = [], 
                  word: str = "") -> int:
    
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
                 index: int = 0, 
                 _tokens_:List[Tuple[str, str, int]] = [], 
                 word: str = "") -> int:
    
    if index >= len(linha): 
        _tokens_.append(("NUM", word, index - len(word)))
        return estadoEntrada, index, _tokens_, ""
    
    if linha[index].isdecimal():
        return estadoNumero, index+1, _tokens_, word + linha[index]
    
    if linha[index] == '.':
        return estadoPonto, index+1, _tokens_, word + linha[index]

    _tokens_.append(("NUM", word, index - len(word)))
    return estadoEntrada, index, _tokens_, ""

def estadoPonto(linha: str, 
                index: int = 0, 
                _tokens_:List[Tuple[str, str, int]] = [], 
                word: str = "") -> int:
    
    ...

def estadoDecimal(linha: str, 
                  index: int = 0, 
                  _tokens_:List[Tuple[str, str, int]] = [], 
                  word: str = "") -> int:
    
    ...


def estadoOperador(linha: str, 
                   index: int = 0, 
                   _tokens_:List[Tuple[str, str, int]] = [], 
                   word: str = "") -> int:
    
    ...

def estadoDivisao(linha: str, 
                  index: int = 0, 
                  _tokens_:List[Tuple[str, str, int]] = [], 
                  word: str = "") -> int:
    
    ...
    

def estadoWhiteSpace(linha: str, 
                     index: int = 0, 
                     _tokens_:List[Tuple[str, str, int]] = [], 
                     word: str = "") -> int:
    
    ...

def estadoLPAREN(linha: str, 
                 index: int = 0, 
                 _tokens_:List[Tuple[str, str, int]] = [], 
                 word: str = "") -> int:
    
    ...
    
def estadoRPAREN(linha: str, 
                 index: int = 0, 
                 _tokens_:List[Tuple[str, str, int]] = [], 
                 word: str = "") -> int:
    
    ...

def estadoR(linha: str, 
            index: int = 0, 
            _tokens_:List[Tuple[str, str, int]] = [], 
            word: str = "") -> int:
    
    ...
    

def estadoE(linha: str,
            index: int = 0, 
            _tokens_:List[Tuple[str, str, int]] = [], 
            word: str = "") -> int:
    
    ...
    
def estadoS(linha: str,
            index: int = 0, 
            _tokens_:List[Tuple[str, str, int]] = [], 
            word: str = "") -> int:
    
    ...

def estadoMEM(linha: str, 
              index: int = 0, 
              _tokens_:List[Tuple[str, str, int]] = [], 
              word: str = "") -> int:
    
    ...