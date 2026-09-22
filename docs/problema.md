# [P4-ETAPA-01] Proposta do problema

**Aluno:** Eduardo Alves Carvalho — 20241002803320

## 1. Descrição do problema

Quando um cliente fecha a compra em um supermercado, o valor a pagar não é
apenas a soma dos preços dos produtos. Sobre os itens incidem promoções, e é a
aplicação dessas promoções que determina o total.

O problema é o **fechamento de uma compra**: dado o que o cliente levou e as
promoções vigentes, calcular quanto ele deve pagar e mostrar como se chegou a
esse valor.

O mesmo problema aparece em qualquer sistema de caixa: comércio eletrônico,
lanchonete com combos, bilheteria. A parte difícil não é a conta, e sim que as
promoções se aplicam a conjuntos de unidades do mesmo produto, e a quantidade
comprada quase nunca é múltiplo exato do que a promoção pede.

## 2. Objetivo

O sistema deve receber um catálogo de produtos e um carrinho de compras e
calcular o valor total, mostrando o detalhamento por produto.

Ele deve:

- identificar cada produto do carrinho no catálogo;
- somar as quantidades quando o mesmo produto aparecer mais de uma vez;
- calcular o valor bruto de cada produto;
- aplicar a promoção do produto, quando houver, e calcular o desconto;
- mostrar, por produto, o valor bruto, o desconto e o valor líquido;
- mostrar o subtotal, o total de descontos e o valor final;
- recusar carrinhos inválidos, informando o motivo.

## 3. Entradas

### 3.1 Catálogo

Uma lista de produtos, cada um com:

| Campo | Descrição |
|---|---|
| código | identificador do produto |
| descrição | nome do produto |
| preço unitário | valor positivo com duas casas decimais |
| promoção | a promoção do produto, ou nenhuma |

Cada produto tem no máximo uma promoção, de um destes três tipos:

| Tipo | Parâmetros | Significado |
|---|---|---|
| leve n pague m | n, m inteiros, 0 < m < n | a cada n unidades levadas, cobram-se m |
| percentual acima de | q inteiro, p percentual | atingindo q unidades, aplica-se p% de desconto na linha |
| pacote | k inteiro, v valor | cada k unidades custam v |

### 3.2 Carrinho

Uma lista de itens, cada um com um código e uma quantidade inteira. O carrinho
pode estar vazio, e o mesmo código pode aparecer mais de uma vez.

### 3.3 Catálogo de referência

Os exemplos desta especificação e os casos de teste da Etapa 02 usam este
catálogo:

| Código | Descrição | Preço | Promoção |
|---|---|---|---|
| CAFE | Café torrado 500 g | 18,00 | leve 3 pague 2 |
| ARROZ | Arroz tipo 1, 5 kg | 24,50 | 10% a partir de 4 unidades |
| FEIJAO | Feijão carioca 1 kg | 8,00 | nenhuma |
| SABAO | Sabão em pó 1 kg | 12,00 | 2 por 20,00 |
| SUCO | Suco de uva 1 L | 7,99 | 10% a partir de 3 unidades |

## 4. Saídas

Quando o carrinho é válido, o sistema produz:

1. uma linha por produto, com código, descrição, quantidade, valor bruto,
   desconto, promoção aplicada e valor líquido;
2. o subtotal, somando os valores brutos;
3. o total de descontos;
4. o total a pagar.

Quando o carrinho é inválido, o sistema informa o erro e não produz o
detalhamento.

## 5. Regras do problema

**R1.** Itens com o mesmo código têm suas quantidades somadas em uma única
linha.

**R2.** As linhas aparecem na ordem da primeira vez que o código foi citado no
carrinho.

**R3.** O valor bruto de uma linha é a quantidade multiplicada pelo preço
unitário.

**R4.** Cada produto tem no máximo uma promoção, e promoções não se acumulam.
Produto sem promoção tem desconto zero.

**R5 (leve n pague m).** Sendo `q` a quantidade e `g` o número de grupos
completos de `n` unidades, cobram-se `g × m + (q − g × n)` unidades. As unidades
que sobram são cobradas normalmente.

**R6 (percentual acima de).** Se a quantidade for maior ou igual a `q`, o
desconto é `p%` do valor bruto da linha. Abaixo disso não há desconto.

**R7 (pacote).** Sendo `g` o número de pacotes completos de `k` unidades, a
linha custa `g × v + (q − g × k) × preço unitário`. As unidades fora dos pacotes
são cobradas normalmente.

**R8.** Os valores têm duas casas decimais. Quando o cálculo do desconto der
mais casas, arredonda-se o desconto para duas, meio para cima. O líquido é o
bruto menos o desconto já arredondado.

**R9.** Carrinho vazio é válido: produz uma apuração sem linhas, com total
0,00.

**R10.** O carrinho é inválido quando um código não existe no catálogo ou
quando uma quantidade não é um inteiro maior que zero. Nesse caso nada é
apurado, e o sistema relata o primeiro problema encontrado.

## 6. Casos de exemplo

Usando o catálogo de referência.

**E1 — produto sem promoção.** `FEIJAO × 2`
→ bruto 16,00, desconto 0,00, **total 16,00**

**E2 — leve 3 pague 2, quantidade exata.** `CAFE × 3`
3 unidades formam um grupo, cobram-se 2.
→ bruto 54,00, desconto 18,00, **total 36,00**

**E3 — leve 3 pague 2, com sobra.** `CAFE × 5`
Um grupo de 3 (cobra 2) e 2 unidades soltas: cobram-se 4.
→ bruto 90,00, desconto 18,00, **total 72,00**

**E4 — pacote com sobra.** `SABAO × 5`
Dois pacotes de 2 por 20,00 e uma unidade solta a 12,00.
→ bruto 60,00, desconto 8,00, **total 52,00**

**E5 — carrinho misto.** `CAFE × 2`, `ARROZ × 4`, `FEIJAO × 1`, `CAFE × 1`
Os dois lançamentos de CAFE somam 3 unidades (R1). ARROZ atinge 4 unidades e
recebe 10% sobre 98,00.

| Produto | Qtd | Bruto | Desconto | Líquido |
|---|---|---|---|---|
| CAFE | 3 | 54,00 | 18,00 | 36,00 |
| ARROZ | 4 | 98,00 | 9,80 | 88,20 |
| FEIJAO | 1 | 8,00 | 0,00 | 8,00 |

→ subtotal 160,00, descontos 27,80, **total 132,20**

## 7. Casos-limite

**L1 — carrinho vazio.** Sem itens. O resultado é uma apuração sem linhas e
total 0,00. Carrinho vazio não é erro.

**L2 — quantidade no limiar.** `ARROZ × 3` não recebe desconto (73,50);
`ARROZ × 4` recebe (88,20). O limiar de R6 inclui o próprio valor.

**L3 — código inexistente.** `CAFE × 2`, `BISCOITO × 1` é recusado, porque
BISCOITO não está no catálogo. Nada é apurado, nem a linha do CAFE.

## 8. Restrições

Está fora do escopo:

- formas de pagamento, troco e parcelamento;
- impostos: os preços já são finais;
- controle de estoque;
- cadastro de produtos: o catálogo é uma entrada;
- cupons, descontos por cliente e programas de fidelidade;
- promoções que combinam produtos diferentes;
- venda por peso: tudo é vendido em unidades inteiras;
- banco de dados, interface gráfica e rede.

## 9. Principais conceitos do domínio

- **Produto** — o que pode ser vendido; tem código, descrição e preço.
- **Catálogo** — o conjunto de produtos conhecidos.
- **Promoção** — a regra que diz quanto se deixa de pagar em função da
  quantidade. É o conceito com mais variedade, já que são três tipos com
  comportamentos diferentes.
- **Item de carrinho** — um código e uma quantidade.
- **Carrinho** — a lista de itens da compra.
- **Linha de apuração** — o resultado por produto: quantidade, bruto, desconto e
  líquido.
- **Apuração** — as linhas mais os totais.
- **Erro de validação** — a recusa do carrinho, com o motivo.

## 10. Adequação aos quatro paradigmas

**Imperativo.** A apuração é uma varredura do carrinho, mantendo totais em
variáveis que são atualizadas a cada item. A soma das quantidades repetidas
(R1) é estado que muda ao longo do laço. O fluxo é sequencial: validar, agregar,
calcular, somar.

**Orientado a objetos.** Os conceitos da seção 9 viram objetos com
responsabilidades próprias. Os três tipos de promoção respondem à mesma pergunta
— quanto de desconto para esta quantidade — de formas diferentes, o que se
resolve com polimorfismo.

**Funcional.** A apuração pode ser escrita como transformações sobre dados que
não mudam: agrupar os itens, mapear cada grupo em uma linha, reduzir as linhas
aos totais. A promoção vira uma função que recebe quantidade e preço e devolve o
desconto.

**Lógico.** As regras R5, R6 e R7 já estão escritas como relações entre
promoção, quantidade e desconto. A apuração pode ser feita consultando fatos (o
catálogo) contra regras (as promoções), e a ausência de promoção é simplesmente
a ausência de uma cláusula.

## 11. Linguagens inicialmente consideradas

| Paradigma | Linguagem | Justificativa |
|---|---|---|
| Imperativo | Python | Variáveis, laços e funções diretos, o que deixa o fluxo de execução visível. É a linguagem que mais conheço, o que reduz o risco de erro. |
| Orientado a objetos | Python | Classes, herança e polimorfismo sem estrutura obrigatória em volta. Usando a mesma linguagem do imperativo, fica claro que o que mudou foi a organização da solução. |
| Funcional | Python (a confirmar) | Tem funções de primeira classe, `map`, `filter` e `reduce`. A ressalva é que não obriga imutabilidade, então o caráter funcional depende de disciplina ao escrever. Haskell e Elixir seguem em avaliação. |
| Lógico | Prolog (em aberto) | É a linguagem em que unificação e backtracking são o próprio modelo de execução, e não uma biblioteca. Como o paradigma ainda será estudado na disciplina, a decisão fica em aberto. |
