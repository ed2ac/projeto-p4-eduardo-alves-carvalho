# [P4-ETAPA-03] Implementação imperativa

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Decisões de implementação da solução em [`imperativo/`](../imperativo/).
Linguagem: Python. Arquivos: `caixa.py` (solução) e `testes_casos.py`
(validação contra a Etapa 02).

## Estados mantidos

A solução mantém quatro estados, todos criados dentro de `apurar` e vivos
apenas durante uma apuração:

| Estado | Onde | O que guarda |
|---|---|---|
| `ordem` | `agregar_itens` | a sequência dos códigos, na ordem da primeira aparição (R2) |
| `quantidades` | `agregar_itens` | a quantidade acumulada por código (R1) |
| `linhas` | `apurar` | as linhas do comprovante, montadas uma a uma |
| `totais` | `apurar` | os acumuladores de subtotal, descontos e total |

O catálogo (`CATALOGO`) também é estado, mas é estado **de leitura**: nenhuma
função o altera. Ele é passado como parâmetro para `apurar` e `validar_carrinho`
em vez de ser lido diretamente da variável global, para que fique explícito de
onde o dado vem.

## Operações que modificam estado

- `agregar_itens` — acrescenta a `ordem` e soma em `quantidades`, dentro do
  laço que percorre o carrinho.
- `apurar` — acrescenta a `linhas` a cada produto processado.
- `acumular_totais` — soma o bruto e o desconto de uma linha nos três campos de
  `totais`.

As demais funções (`calcular_desconto`, `descrever_promocao`, `formatar`,
`validar_carrinho`) não alteram nada: recebem valores e devolvem um resultado.

## Efeitos colaterais

Há dois lugares, e os dois são deliberados:

**`acumular_totais(totais, bruto, desconto)`** modifica o dicionário recebido
por parâmetro, em vez de devolver um dicionário novo. Quem chama não usa o
retorno — usa o fato de que o argumento mudou. É o efeito colateral típico do
paradigma imperativo: um subprograma que existe para alterar um estado
compartilhado.

**`imprimir_apuracao(resultado)`** escreve na saída padrão. É efeito colateral
sobre o ambiente externo, e por isso ficou separado do cálculo: `apurar` devolve
os dados e não imprime nada. Assim a mesma apuração pode ser impressa,
comparada em teste ou descartada.

A separação entre as duas é intencional. `apurar` pode ser chamada pelo
`testes_casos.py` sem produzir nenhuma saída de tela.

## Estruturas de controle

- **`while` em `validar_carrinho`** — a varredura precisa **parar no primeiro
  item inválido** (R10), e o `while` com índice explícito deixa essa
  interrupção visível, já que a condição de parada aparece no cabeçalho do laço
  e o avanço do índice é escrito à mão.
- **`for` nos demais laços** — em `agregar_itens` e em `apurar` todos os itens
  são percorridos sempre, sem saída antecipada, então o `for` sobre a coleção é
  suficiente.
- **`if` encadeado em `calcular_desconto`** — cada tipo de promoção tem sua
  fórmula (R5, R6, R7), e o encadeamento de `if` seleciona qual aplicar. O caso
  `promocao is None` é tratado logo na entrada, o que evita repetir a
  verificação dentro de cada ramo.
- **Retorno antecipado em `apurar`** — quando a validação falha, a função
  retorna ali mesmo. Nada é apurado, como manda a R10.

## Organização dos subprogramas

Cada função faz uma etapa do fluxo, e `apurar` é quem as encadeia:

```
apurar
  ├── validar_carrinho      recusa o carrinho, ou libera
  ├── agregar_itens         soma quantidades e fixa a ordem
  └── para cada codigo:
        ├── calcular_desconto     aplica a regra da promocao
        ├── descrever_promocao    texto da promocao para a linha
        └── acumular_totais       soma nos acumuladores
```

`formatar` e `imprimir_apuracao` ficam fora desse encadeamento porque são
apresentação, não cálculo.

Os parâmetros seguem duas regras: o que é lido entra por valor
(`quantidade`, `preco`, `promocao`), e o que é modificado entra como a estrutura
a ser alterada (`totais`). Quem lê a assinatura consegue prever se a chamada vai
mudar alguma coisa.

## Por que a solução é predominantemente imperativa

- O resultado é construído **modificando estado ao longo do tempo**, e não
  descrevendo uma expressão. `totais` começa zerado e vai sendo somado; `linhas`
  começa vazia e vai crescendo. Em nenhum momento existe uma expressão única que
  descreva o total.
- O **fluxo é explícito e sequencial**: validar, agregar, calcular, acumular,
  nessa ordem. Trocar a ordem quebra a solução, porque cada passo depende do
  estado deixado pelo anterior.
- A decomposição é por **procedimento**, e não por entidade. Não existe
  `Produto`, `Carrinho` ou `Promocao` como objeto: existem funções que operam
  sobre dados simples (dicionários e tuplas).
- **Não há classes, herança nem polimorfismo.** A escolha entre os três tipos de
  promoção é feita por um encadeamento de `if` sobre o primeiro elemento da
  tupla — exatamente o ponto que a versão orientada a objetos deverá substituir
  por despacho dinâmico.
- Há um subprograma cuja finalidade é **alterar o estado de quem chamou**
  (`acumular_totais`), o que só faz sentido em um modelo com estado mutável
  compartilhado.

## Outras decisões

**Valores em centavos.** Todo valor monetário é um inteiro de centavos, e a
conversão para texto acontece só na apresentação (`formatar`). A alternativa
seria usar ponto flutuante, que introduziria erro de representação em valores
como 7,99. Com inteiros, o arredondamento da R8 vira uma divisão inteira:
`(bruto * percentual + 50) // 100`, em que o `+ 50` produz o arredondamento meio
para cima.

**`bool` descartado na validação.** Em Python `bool` é subtipo de `int`, de modo
que `isinstance(True, int)` é verdadeiro e `True` passaria como quantidade 1. A
validação descarta `bool` explicitamente.

**Erro devolvido, não levantado.** `validar_carrinho` devolve uma mensagem de
texto em vez de lançar exceção, e `apurar` devolve um resultado com o campo
`erro` preenchido. Mantém o fluxo de controle visível: o desvio acontece por um
`if` que se lê na função, e não por um mecanismo que salta de um ponto a outro
do programa.

## Validação

`imperativo/testes_casos.py` roda os 15 casos da Etapa 02
([`../testes/casos.md`](../testes/casos.md)) contra esta implementação,
conferindo subtotal, descontos e total. Nos casos N10 e F01 confere também a
quantidade e a ordem das linhas, que são as regras R1 e R2.

```
$ python testes_casos.py
...
15 casos: 15 aprovados, 0 reprovados
```
