# RA1 2 - Analisador Léxico e Gerador de Assembly ARMv7

**Instituição:** PUCPR
**Disciplina:** Construção de Interpretadores
**Professor:** Frank Alcantara
**Grupo no Canvas:** RA1 2

## Integrantes

| Nome | GitHub |
|------|--------|
| Gabriel Vidal Schneider | [@Gabiru1089](https://github.com/Gabiru1089) |
| Lucca Fabricio Magalhães | [@luccafm1](https://github.com/luccafm1) |
| Mohamad Kassem Diab | [@Mo1409](https://github.com/Mo1409) |
| Vinícius Yamamoto Borges | [@Vini-y](https://github.com/Vini-y) |

---

## Descrição

Programa em Python que lê expressões aritméticas em notação polonesa reversa (RPN),
realiza análise léxica via Autômato Finito Determinístico (AFD) e gera código Assembly ARMv7
compatível com o simulador CPUlator DEC1-SOC (v16.1).

O código Python apenas lê o arquivo, faz a análise léxica e gera o Assembly.
Todos os cálculos são realizados no Assembly gerado, executado no CPUlator.

## Operações suportadas

| Operação | Sintaxe | Exemplo |
|----------|---------|---------|
| Adição | `(A B +)` | `(3.14 2.0 +)` |
| Subtração | `(A B -)` | `(10 5 -)` |
| Multiplicação | `(A B *)` | `(2.5 4.0 *)` |
| Divisão real | `(A B /)` | `(9.0 3.0 /)` |
| Divisão inteira | `(A B //)` | `(10 3 //)` |
| Resto | `(A B %)` | `(10 3 %)` |
| Potenciação | `(A B ^)` | `(2.0 8 ^)` |

Comandos especiais:

- `(V MEM)` — armazena o valor V na variável MEM
- `(MEM)` — retorna o valor armazenado em MEM
- `(N RES)` — retorna o resultado de N linhas anteriores

Expressões podem ser aninhadas: `((1.5 2.0 *) (3.0 4.0 *) /)`

## Estrutura do projeto

```
RA1-2/
├── src/
│   ├── main.py        # Ponto de entrada - Aluno 4 - Mohamad
│   ├── lexer.py       # AFD e parseExpressao - Aluno 1 - Lucca
│   ├── executor.py    # Execução RPN e memória - Aluno 2 - Gabriel
│   ├── assembly.py    # Geração Assembly e lerArquivo - Aluno 3 - Vinícius
│   └── display.py     # Exibição de resultados - Aluno 4 - Mohamad
├── testes/
│   ├── teste1.txt     # 12 expressões
│   ├── teste2.txt     # 13 expressões
│   └── teste3.txt     # 13 expressões
├── assembly/
│   └── assembly.s     # Último Assembly gerado
├── tokens.txt         # Tokens da última execução (CSV)
└── README.md
```

## Como executar

```bash
python src/main.py testes/teste1.txt
```

O programa gera:
- `tokens.txt` — tokens da última execução em formato CSV
- `assembly/assembly.s` — código Assembly ARMv7 gerado

## Como rodar os testes de cada módulo

```bash
python src/assembly.py  # testes do gerador de Assembly e leitura de arquivo
```

## Como testar no CPUlator

1. Acesse https://cpulator.01xz.net/?sys=arm-de1soc
2. Selecione **ARMv7 DEC1-SOC (v16.1)**
3. Carregue `assembly/assembly.s`
4. Clique em **Compile and Load** e depois **Continue (F3)**
5. O resultado de cada expressão aparece no **JTAG UART** com uma casa decimal
