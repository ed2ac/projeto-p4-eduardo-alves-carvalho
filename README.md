# Projeto P4 — Um problema, quatro paradigmas

**Disciplina:** Paradigmas de Linguagens de Programação
**Aluno:** Eduardo Alves Carvalho — 20241002803320

Resolução de um mesmo problema nos quatro paradigmas estudados na disciplina:
imperativo, orientado a objetos, funcional e lógico.

## O problema

**Fechamento de uma compra com promoções.** Dado um catálogo de produtos com
suas promoções e um carrinho de compras, calcular o valor a pagar e mostrar o
detalhamento por produto.

A especificação está em [`docs/problema.md`](docs/problema.md).

## Etapas entregues

- **[P4-ETAPA-01] Proposta do problema** — [`docs/problema.md`](docs/problema.md)
- **[P4-ETAPA-02] Contrato semântico e testes** — [`testes/casos.md`](testes/casos.md)
- **[P4-ETAPA-03] Implementação imperativa** — [`imperativo/`](imperativo/), decisões em [`docs/decisoes.md`](docs/decisoes.md)

## Estrutura

```
projeto-p4-eduardo-alves-carvalho/
├── README.md
├── docs/
│   ├── problema.md          especificação do problema
│   └── decisoes.md          decisões de implementação
├── testes/
│   └── casos.md             casos de teste
├── imperativo/
│   ├── caixa.py             solução
│   └── testes_casos.py      validação contra os casos da Etapa 02
├── poo/
├── funcional/
├── logico/
└── integrado/
```

## Linguagens

Python nos paradigmas imperativo, orientado a objetos e funcional. O paradigma
lógico deve usar Prolog, mas a decisão fica em aberto até a etapa
correspondente. A justificativa de cada escolha está na seção 11 de
[`docs/problema.md`](docs/problema.md).
