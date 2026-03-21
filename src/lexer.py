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
    
    
    
    return None # <- token inválido
