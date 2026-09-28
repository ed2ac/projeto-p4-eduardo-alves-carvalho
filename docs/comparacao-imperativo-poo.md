# [P4-ETAPA-05] Comparação entre imperativo e POO

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Comparação entre [`imperativo/caixa.py`](../imperativo/caixa.py) (Etapa 03) e
[`poo/caixa.py`](../poo/caixa.py) (Etapa 04), que resolvem o mesmo problema e
passam nos mesmos 15 casos da Etapa 02.

## Medidas do código

Os números abaixo foram contados nos dois arquivos, e não estimados. O `if` do
rodapé (`if __name__ == "__main__"`) está descontado, por não ser lógica do
problema.

| | imperativo | POO |
|---|---|---|
| linhas de código | 120 | 200 |
| classes | 0 | 13 |
| funções no nível do módulo | 9 | 2 |
| métodos | — | 49 |
| `if` de lógica | 15 | 6 |
| `for` | 4 | 4 |
| `while` | 1 | 0 |
| `raise` | 0 | 4 |
| arquivo de testes | 68 linhas | 66 linhas |

Um número explica boa parte da comparação: dos 15 `if` da versão imperativa,
**9 existiam só para escolher o tipo de promoção** — 5 em `calcular_desconto` e
4 em `descrever_promocao`. Na versão orientada a objetos esses 9 desapareceram,
e os outros 6 continuaram exatamente 6. O que a orientação a objetos eliminou
não foi condicional em geral: foi **condicional sobre tipo**.

## Os doze aspectos

### Representação do estado

Na versão imperativa o estado são quatro estruturas soltas dentro de `apurar`:
`ordem`, `quantidades`, `linhas` e o dicionário `totais`. Nenhuma delas tem
identidade própria — são variáveis locais que existem enquanto a função roda.

Na versão orientada a objetos o estado tem nome e dono. `Linha` guarda o
resultado de um produto; `Apuracao` guarda as linhas; `Dinheiro` guarda
centavos. O dicionário `totais` simplesmente deixou de existir: `Apuracao`
calcula subtotal, descontos e total a partir das linhas, em vez de mantê-los em
paralelo.

### Mutabilidade

A versão imperativa é mutável por construção: `totais` é atualizado a cada
volta do laço, `quantidades` é somado item a item, `linhas` cresce por
`append`.

A versão orientada a objetos é quase toda imutável, sem que isso tenha sido um
objetivo declarado. `Dinheiro` não tem operação que altere o próprio valor —
`__add__` e `vezes` devolvem novos objetos. `Linha` calcula tudo no construtor.
As únicas coisas que mudam depois de criadas são a lista de lançamentos do
`Carrinho` e o dicionário interno do `Catalogo`.

### Fluxo de controle

Na versão imperativa o fluxo está escrito em um lugar só, em ordem:
`validar_carrinho`, `agregar_itens`, laço sobre os códigos, `acumular_totais`.
Lendo `apurar` de cima a baixo você vê o algoritmo inteiro.

Na versão orientada a objetos o fluxo está distribuído. `Carrinho.apurar`
constrói as `Linha`, cada `Linha` pergunta ao `Produto`, cada `Produto` delega à
sua `Promocao`. Não existe um lugar onde o algoritmo esteja escrito por
inteiro — ele emerge da colaboração. É mais fácil de estender e mais difícil de
acompanhar pela primeira vez.

### Decomposição do problema

Imperativa: decomposição **por etapa do processamento**. As nove funções são
nove passos — validar, agregar, calcular, acumular, formatar, imprimir.

Orientada a objetos: decomposição **por conceito do domínio**. As treze classes
são os conceitos da seção 9 da especificação, quase um para um. Vale notar que
a especificação da Etapa 01 já listava esses conceitos, e a versão imperativa
simplesmente não os usou como unidade de organização.

### Reutilização

Na versão imperativa, reutilizar é chamar a mesma função: `formatar` é usada em
seis lugares de `imprimir_apuracao`.

Na versão orientada a objetos, o que se reutiliza é um **tipo**: `Dinheiro`
aparece em `Produto`, nas quatro promoções, em `Linha` e em `Apuracao`. A
diferença prática é a garantia: reutilizar uma função não impede que alguém some
dois inteiros que não eram dinheiro; reutilizar `Dinheiro` impede.

As quatro subclasses de `Promocao` **não compartilham código entre si**, apenas
o contrato. As fórmulas são genuinamente diferentes, e forçar código comum ali
seria inventar reutilização onde não há.

### Manutenção

Depende do tipo de mudança, e é aqui que a troca fica evidente.

| Mudança | Imperativo | POO |
|---|---|---|
| corrigir a fórmula de uma promoção | 1 ramo de `calcular_desconto` | 1 método de 1 classe |
| acrescentar um tipo de promoção | 2 funções existentes mudam | 1 classe nova, nada existente muda |
| mudar a assinatura do cálculo de desconto | 1 função | 4 subclasses |
| mudar o formato de impressão | 1 função | `__str__` de `Linha` e de `Apuracao` |

### Facilidade de extensão

É a vantagem mais clara da versão orientada a objetos, e é mensurável.
Acrescentar uma promoção "desconto fixo por unidade" custa:

- **imperativo**: abrir `calcular_desconto` e acrescentar um ramo; abrir
  `descrever_promocao` e acrescentar outro. Duas funções que já funcionavam são
  editadas, e cada edição pode quebrar o que já estava lá.
- **POO**: escrever uma classe com dois métodos. Nenhum arquivo existente é
  tocado.

### Tratamento de erros

Mudou de mecanismo, e não só de forma. A versão imperativa **devolve** o erro:
`validar_carrinho` retorna uma string ou `None`, e `apurar` devolve um
dicionário com o campo `erro` preenchido. São 0 `raise` no arquivo inteiro.

A versão orientada a objetos **levanta** exceções — `ProdutoInexistente` e
`QuantidadeInvalida`, 4 `raise` no total. E a validação mudou de momento: antes
acontecia toda de uma vez, no começo de `apurar`; agora acontece em
`Carrinho.lancar`, no instante do lançamento. Um carrinho orientado a objetos
**não chega a existir** em estado inválido.

O mesmo vale para `LeveNPagueM.__init__`, que recusa `0 < m < n` violado. Na
versão imperativa a tupla `("leve_n_pague_m", 3, 2)` podia ser montada errada e
só falharia no cálculo.

### Efeitos colaterais

Na versão imperativa há dois, ambos deliberados: `acumular_totais` modifica o
dicionário recebido por parâmetro, e `imprimir_apuracao` escreve na saída.

Na versão orientada a objetos o primeiro desapareceu — não há acumulador para
modificar. Restou a impressão, agora na forma de `__str__`, que é ainda mais
contida: `__str__` devolve texto, e quem imprime é o `main`. O cálculo ficou
livre de efeito colateral nos dois casos, mas na versão orientada a objetos isso
é consequência do desenho, não uma disciplina que o autor precisou manter.

### Facilidade para testar

Surpreendentemente parecida: 68 linhas contra 66 no arquivo de testes, com os
mesmos 15 casos. Isso acontece porque as duas implementações foram desenhadas
com o cálculo separado da apresentação, e não porque um paradigma ajude mais.

Onde diferem é no que dá para testar **isoladamente**. Na versão orientada a
objetos é possível instanciar `LeveNPagueM(3, 2)` e testar só ela, sem carrinho,
sem catálogo e sem produto. Na versão imperativa, `calcular_desconto` também é
testável isolada, mas exige montar a tupla certa — e nada impede montar uma
tupla que não corresponde a promoção nenhuma.

### Organização do código

Imperativa: um arquivo, nove funções, ordem de leitura igual à ordem de
execução. Cabe na cabeça de uma vez.

Orientada a objetos: um arquivo, treze classes agrupadas por papel — valor,
promoções, domínio, apuração. A ordem de leitura não é mais a de execução, e
entender `apurar` exige pular entre quatro classes.

### Complexidade

A versão orientada a objetos tem **67% mais linhas de código** (200 contra 120)
para resolver exatamente o mesmo problema, com exatamente o mesmo resultado —
as duas foram comparadas em 4.000 carrinhos aleatórios, sem divergência.

Esse custo não é desperdício nem virtude por si: é o preço de tornar a extensão
barata. Em um problema que nunca fosse estendido, seriam 80 linhas a mais sem
retorno algum.

## As seis perguntas

### 1. Qual problema ficou mais fácil de expressar de forma imperativa?

**A totalização.** Somar três acumuladores dentro do laço que já percorre os
produtos é a expressão direta do que se quer: o corpo de `acumular_totais` são três atribuições.

Na versão orientada a objetos, `Apuracao.subtotal`, `descontos` e `total` são
propriedades que percorrem as linhas **a cada acesso**. Medindo: uma única
impressão percorre a lista de linhas **4 vezes**, porque `__str__` lê as três
propriedades e `total` por sua vez lê `subtotal` e `descontos` de novo. A versão
imperativa percorria uma vez só. Para 5 produtos não importa; a observação é que
o modelo mais limpo aqui é também o menos direto.

**A agregação** também: `agregar_itens` faz exatamente o que diz, sem
intermediário. O equivalente orientado a objetos, `Carrinho.agrupado`, é
praticamente o mesmo código dentro de um método — ou seja, aqui a orientação a
objetos não acrescentou nem tirou nada.

### 2. Qual problema ficou mais fácil de expressar utilizando orientação a objetos?

**As três promoções.** Na versão imperativa, uma promoção é uma tupla cujo
primeiro elemento é um rótulo, e duas funções separadas precisam saber
interpretar esse rótulo — daí os 9 `if`. O conhecimento sobre "o que é uma
promoção leve-n-pague-m" fica espalhado por dois lugares que precisam ser
mantidos em sincronia.

Na versão orientada a objetos, cada promoção é uma classe que sabe calcular o
próprio desconto e descrever a si mesma. O conhecimento fica em um lugar só.

### 3. Onde a orientação a objetos realmente trouxe vantagem?

Em dois pontos concretos, e não em geral:

- **Extensão por tipo novo.** Acrescentar uma promoção não toca em código
  existente. É o ganho mais claro e o mais fácil de demonstrar.
- **Impossibilitar estados inválidos.** `Dinheiro` não deixa somar dinheiro com
  número solto; `LeveNPagueM` recusa parâmetros incoerentes no construtor;
  `Carrinho.lancar` recusa o lançamento inválido antes de guardá-lo. Na versão
  imperativa todos esses erros eram possíveis de montar e só apareciam depois.

### 4. Em quais situações a utilização de objetos acrescentou complexidade desnecessária?

Duas, e vale reconhecê-las em vez de defender o paradigma:

- **`Dinheiro`.** São cerca de 40 linhas de classe para encapsular um inteiro.
  O ganho real — impedir somar dinheiro com não-dinheiro — é pequeno num
  programa deste tamanho, em que todos os valores já eram centavos por
  convenção. A classe se paga em um sistema grande; aqui é quase cerimônia.
- **`SemPromocao`.** Uma classe inteira para devolver zero. Ela evita um `if` em
  `Produto`, mas troca um condicional de uma linha por um arquivo a mais de
  conceito para o leitor entender. É defensável, não é obviamente melhor que
  `if promocao is None: return 0`.

Também merece nota que `Produto` tem três `@property` que só devolvem o atributo
privado. É o encapsulamento pedido pela etapa, mas em Python isso é
frequentemente ruído.

### 5. Que partes do problema praticamente não mudaram entre as duas implementações?

**A aritmética das promoções.** As três fórmulas são as mesmas nos dois
arquivos, só que uma em função e outra em método. O arredondamento é literalmente
a mesma expressão:

```
imperativo/caixa.py:115    return (bruto * percentual + 50) // 100
poo/caixa.py:40            return Dinheiro((self._centavos * p + 50) // 100)
```

**A agregação por código** também: o laço que monta `ordem` e soma quantidades é
o mesmo nas duas versões.

Isso é esperado, e é um bom sinal: essas partes são **as regras do problema**,
definidas na Etapa 01. Elas não deveriam mesmo depender do paradigma. O que muda
é onde elas moram, não o que elas dizem.

### 6. Que partes precisaram ser completamente remodeladas?

Três, em ordem de profundidade:

- **A escolha do tipo de promoção.** Deixou de ser um encadeamento de `if` sobre
  um rótulo e virou despacho dinâmico. É a mudança que os números mostram: 9 `if`
  a menos.
- **A totalização.** Deixou de ser acumulador e virou valor derivado. O
  dicionário `totais` não tem equivalente na versão orientada a objetos — ele
  simplesmente deixou de ser necessário.
- **O tratamento de erros.** Deixou de ser valor de retorno e virou exceção, e
  mudou de momento: da apuração para o lançamento.

O que não mudou, e talvez seja o achado mais útil deste exercício, é **a
especificação**. Os 15 casos da Etapa 02 valeram sem uma linha de alteração para
as duas implementações. Um contrato escrito sem falar de implementação sobrevive
à troca de paradigma — que era exatamente o que a Etapa 02 se propunha a testar.
