# [P4-ETAPA-05] Comparação entre imperativo e POO

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Comparação entre [`imperativo/caixa.py`](../imperativo/caixa.py) e
[`poo/caixa.py`](../poo/caixa.py). As duas passam nos mesmos 15 casos da
Etapa 02.

## Aspectos

**Representação do estado.** No imperativo, variáveis locais em `apurar`
(`linhas`, `subtotal`, `descontos`). Na POO, atributos dos objetos (`Carrinho`,
`Linha`, `Apuracao`).

**Mutabilidade.** No imperativo os acumuladores mudam a cada volta do laço. Na
POO só a lista de itens do `Carrinho` muda; `Linha` e `Apuracao` calculam tudo
na criação.

**Fluxo de controle.** No imperativo o fluxo inteiro está em `apurar`, de cima
para baixo. Na POO ele passa por vários objetos: `Carrinho` cria as `Linha`,
que pedem o desconto ao `Produto`, que pede à `Promocao`.

**Decomposição do problema.** No imperativo, por etapas (validar, agrupar,
calcular, imprimir). Na POO, pelos conceitos do domínio (produto, promoção,
carrinho, linha, apuração).

**Reutilização.** No imperativo, reutiliza-se chamando as mesmas funções. Na
POO, o `Produto` funciona com qualquer subclasse de `Promocao`.

**Manutenção.** Corrigir a fórmula de uma promoção é igualmente fácil nos dois:
no imperativo é um ramo do `if`, na POO é o método de uma classe.

**Facilidade de extensão.** Na POO uma promoção nova é uma classe nova, sem
mexer no resto. No imperativo é preciso alterar `calcular_desconto`.

**Tratamento de erros.** No imperativo, `validar` devolve a mensagem de erro e
`apurar` repassa. Na POO, `Catalogo.buscar` e `Carrinho.adicionar` lançam
`ValueError`.

**Efeitos colaterais.** Nos dois, só a impressão escreve na tela; o cálculo
não.

**Facilidade para testar.** Parecida: os dois arquivos de teste rodam os
mesmos 15 casos da mesma forma.

**Organização do código.** O imperativo tem 5 funções mais `formatar`; a POO
tem 9 classes.

**Complexidade.** A versão imperativa é mais curta e mais fácil de ler de uma
vez. A POO tem mais código, mas cada parte é menor.

## Perguntas

**1. Qual problema ficou mais fácil de expressar de forma imperativa?**
Somar os totais e agrupar os itens repetidos: é só um laço atualizando
variáveis.

**2. Qual problema ficou mais fácil de expressar utilizando orientação a
objetos?** As promoções. Cada tipo virou uma classe com seu próprio cálculo, em
vez de um `if` que testa o tipo.

**3. Onde a orientação a objetos realmente trouxe vantagem?** Na extensão:
acrescentar uma promoção nova não altera o código que já existe.

**4. Em quais situações a utilização de objetos acrescentou complexidade
desnecessária?** Nas classes `Linha` e `Apuracao`, que só guardam valores
calculados; no imperativo uma tupla e duas variáveis resolviam.

**5. Que partes do problema praticamente não mudaram entre as duas
implementações?** As fórmulas das promoções, o agrupamento dos itens repetidos
e o uso de centavos.

**6. Que partes precisaram ser completamente remodeladas?** A escolha do tipo
de promoção (de `if` para polimorfismo) e o tratamento de erros (de mensagem
devolvida para exceção).
