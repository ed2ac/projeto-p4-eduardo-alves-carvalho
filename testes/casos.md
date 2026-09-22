# [P4-ETAPA-02] Contrato semântico e testes

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Casos de teste do problema definido na Etapa 01 ([`../docs/problema.md`](../docs/problema.md)).
Os casos descrevem **o que** o sistema deve fazer, sem depender de linguagem ou
paradigma, e serão usados para validar as quatro implementações.

São 15 casos: 10 normais, 3 de fronteira e 2 de entrada inválida.

## Catálogo usado em todos os casos

| Código | Descrição | Preço | Promoção |
|---|---|---|---|
| CAFE | Café torrado 500 g | 18,00 | leve 3 pague 2 |
| ARROZ | Arroz tipo 1, 5 kg | 24,50 | 10% a partir de 4 unidades |
| FEIJAO | Feijão carioca 1 kg | 8,00 | nenhuma |
| SABAO | Sabão em pó 1 kg | 12,00 | 2 por 20,00 |
| SUCO | Suco de uva 1 L | 7,99 | 10% a partir de 3 unidades |

## Como ler a saída esperada

Cada caso válido indica as linhas da apuração no formato
`código, quantidade, bruto, desconto, líquido`, seguidas do subtotal, do total
de descontos e do total a pagar. Todos os valores têm duas casas decimais.

---

## Casos normais

### N01 — produto sem promoção

- **Entrada:** FEIJAO × 2
- **Saída esperada:** FEIJAO, 2, 16,00, 0,00, 16,00 — subtotal 16,00, descontos 0,00, **total 16,00**
- **Descrição:** produto sem promoção cadastrada. O desconto é zero e o líquido é igual ao bruto.

### N02 — uma única unidade

- **Entrada:** FEIJAO × 1
- **Saída esperada:** FEIJAO, 1, 8,00, 0,00, 8,00 — subtotal 8,00, descontos 0,00, **total 8,00**
- **Descrição:** menor compra possível. Serve para conferir que a apuração funciona com uma unidade só.

### N03 — leve 3 pague 2, quantidade exata

- **Entrada:** CAFE × 3
- **Saída esperada:** CAFE, 3, 54,00, 18,00, 36,00 — subtotal 54,00, descontos 18,00, **total 36,00**
- **Descrição:** a quantidade forma exatamente um grupo da promoção. Cobram-se 2 das 3 unidades (R5).

### N04 — leve 3 pague 2, com sobra

- **Entrada:** CAFE × 5
- **Saída esperada:** CAFE, 5, 90,00, 18,00, 72,00 — subtotal 90,00, descontos 18,00, **total 72,00**
- **Descrição:** um grupo completo (3 unidades, cobra 2) e 2 unidades soltas cobradas normalmente. Total de 4 unidades cobradas.

### N05 — leve 3 pague 2, dois grupos

- **Entrada:** CAFE × 6
- **Saída esperada:** CAFE, 6, 108,00, 36,00, 72,00 — subtotal 108,00, descontos 36,00, **total 72,00**
- **Descrição:** dois grupos completos, sem sobra. Cobram-se 4 unidades. Confirma que a promoção se repete, e não se aplica uma vez só.

### N06 — percentual no limiar

- **Entrada:** ARROZ × 4
- **Saída esperada:** ARROZ, 4, 98,00, 9,80, 88,20 — subtotal 98,00, descontos 9,80, **total 88,20**
- **Descrição:** a quantidade atinge exatamente o limiar de 4 unidades, então o desconto de 10% se aplica (R6).

### N07 — percentual acima do limiar

- **Entrada:** ARROZ × 6
- **Saída esperada:** ARROZ, 6, 147,00, 14,70, 132,30 — subtotal 147,00, descontos 14,70, **total 132,30**
- **Descrição:** acima do limiar, o desconto continua sendo 10% sobre toda a linha, e não apenas sobre as unidades excedentes.

### N08 — pacote exato

- **Entrada:** SABAO × 4
- **Saída esperada:** SABAO, 4, 48,00, 8,00, 40,00 — subtotal 48,00, descontos 8,00, **total 40,00**
- **Descrição:** dois pacotes completos de 2 unidades, a 20,00 cada. Sem unidades soltas.

### N09 — pacote com sobra

- **Entrada:** SABAO × 5
- **Saída esperada:** SABAO, 5, 60,00, 8,00, 52,00 — subtotal 60,00, descontos 8,00, **total 52,00**
- **Descrição:** dois pacotes (40,00) e uma unidade solta a 12,00 (R7). A unidade que sobra não recebe desconto proporcional.

### N10 — carrinho misto com código repetido

- **Entrada:** CAFE × 2, ARROZ × 4, FEIJAO × 1, CAFE × 1
- **Saída esperada:**
  - CAFE, 3, 54,00, 18,00, 36,00
  - ARROZ, 4, 98,00, 9,80, 88,20
  - FEIJAO, 1, 8,00, 0,00, 8,00
  - subtotal 160,00, descontos 27,80, **total 132,20**
- **Descrição:** os dois lançamentos de CAFE somam 3 unidades e viram uma linha só (R1), que aparece na posição da primeira citação (R2). Mais de um produto com promoções diferentes na mesma compra.

---

## Casos de fronteira

### F01 — carrinho vazio

- **Entrada:** nenhum item
- **Saída esperada:** nenhuma linha — subtotal 0,00, descontos 0,00, **total 0,00**
- **Descrição:** carrinho vazio é válido, e não um erro (R9). Existe para evitar que a implementação trate a lista vazia como entrada inválida.

### F02 — quantidade logo abaixo do limiar

- **Entrada:** ARROZ × 3
- **Saída esperada:** ARROZ, 3, 73,50, 0,00, 73,50 — subtotal 73,50, descontos 0,00, **total 73,50**
- **Descrição:** uma unidade a menos que N06. Confirma que o limiar de R6 é inclusivo: com 3 não há desconto, com 4 há. É o ponto em que se erra por um.

### F03 — desconto com três casas decimais

- **Entrada:** SUCO × 3
- **Saída esperada:** SUCO, 3, 23,97, 2,40, 21,57 — subtotal 23,97, descontos 2,40, **total 21,57**
- **Descrição:** 10% de 23,97 dá 2,397, que não cabe em duas casas. O desconto é arredondado para 2,40 e o líquido é calculado a partir dele (R8), de modo que bruto menos desconto sempre bate com o líquido.

---

## Casos de entrada inválida

### X01 — código inexistente no catálogo

- **Entrada:** CAFE × 2, BISCOITO × 1
- **Saída esperada:** erro — o código BISCOITO não existe no catálogo. Nenhuma apuração é produzida.
- **Descrição:** o carrinho inteiro é recusado, inclusive a linha do CAFE, que estava correta (R10).

### X02 — quantidade não positiva

- **Entrada:** FEIJAO × 0
- **Saída esperada:** erro — a quantidade 0 não é um inteiro maior que zero. Nenhuma apuração é produzida.
- **Descrição:** vale igualmente para quantidades negativas. Uma quantidade zerada não é o mesmo que não levar o produto: é um lançamento errado no caixa.

---

## Resumo

| Grupo | Casos | Quantidade |
|---|---|---|
| Normais | N01 a N10 | 10 |
| Fronteira | F01 a F03 | 3 |
| Entrada inválida | X01, X02 | 2 |
| | **Total** | **15** |
