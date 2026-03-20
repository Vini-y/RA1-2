# RA1 2 - Analisador Léxico e Gerador de Assembly ARMv7

**Instituição:** PUCPR  
**Disciplina:** Construção de Interpretadores  
**Professor:** Frank Alcantara

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
realiza análise léxica via Autômato Finito Determinístico e gera código Assembly ARMv7
compatível com o simulador CPUlator DEC1-SOC(v16.1).

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
│   ├── teste1.txt
│   ├── teste2.txt
│   └── teste3.txt
├── assembly/
│   └── output.s       # Último Assembly gerado (atualizado a cada execução)
├── tokens_ultima_execucao.csv  # Tokens da última execução
└── README.md
```

## Como executar

```bash
python src/main.py testes/teste1.txt
```

## Como rodar os testes de cada módulo isoladamente

```bash
python src/lexer.py     # testes do analisador léxico
python src/executor.py  # testes do executor
python src/assembly.py  # testes do gerador de Assembly
```

## Como testar no CPUlator

1. Acesse https://cpulator.01xz.net/?sys=arm-de1soc
2. Selecione **ARMv7 DEC1-SOC (v16.1)**
3. Carregue `assembly/output.s`
4. Clique em **Compile and Load** e depois **Continue (F3)**
