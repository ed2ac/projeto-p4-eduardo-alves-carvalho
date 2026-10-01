# [P4-ETAPA-03] Implementação imperativa

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Decisões da solução em [`imperativo/`](../imperativo/), feita em Python.
`caixa.py` é a solução e `testes_casos.py` roda os casos da Etapa 02.

## Quais estados são mantidos

Dentro de `apurar`: a lista `linhas` e os acumuladores `subtotal` e `descontos`.
Dentro de `agrupar`: a lista `ordem` (ordem em que os códigos apareceram) e o
dicionário `quantidades` (quantidade somada de cada código). O catálogo é só
lido, nunca alterado.

## Quais operações modificam estado

- `agrupar` acrescenta códigos em `ordem` e soma em `quantidades`.
- `apurar` acrescenta cada linha em `linhas` e soma nos acumuladores
  `subtotal` e `descontos`, a cada volta do laço.

## Onde aparecem efeitos colaterais

Em `imprimir`, que escreve na tela. O cálculo (`apurar`) não imprime nada, só
devolve os valores, o que permite usá-lo nos testes.

## Estruturas de controle

- `for` para percorrer o carrinho (em `validar` e `agrupar`) e os produtos (em
  `apurar`).
- `if` encadeado em `calcular_desconto` para escolher a fórmula de cada tipo de
  promoção.
- `return` antecipado em `validar`, que para no primeiro erro, e em `apurar`,
  que não calcula nada se o carrinho for inválido.

## Como os subprogramas foram organizados

Uma função para cada etapa: `validar`, `agrupar`, `calcular_desconto`,
`apurar` (que chama as anteriores) e `imprimir`. `formatar` converte centavos
em texto.

## Por que a solução é predominantemente imperativa

O resultado é construído alterando variáveis dentro de laços, passo a passo, na
ordem validar, agrupar, calcular e somar. Os dados são dicionários e tuplas
simples e não há classes; o tipo da promoção é escolhido com `if`.

## Outras decisões

Os valores são guardados em centavos (inteiros) para não ter erro de
arredondamento com números decimais. O arredondamento da regra R8 fica
`(bruto * percentual + 50) // 100`.

## Validação

```
$ python testes_casos.py
...
15 de 15 casos aprovados
```
