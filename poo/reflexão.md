# [P4-ETAPA-04] Implementação orientada a objetos

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Como meu modelo mudou ao passar do paradigma imperativo para o orientado a
objetos. A implementação está em [`caixa.py`](caixa.py) e a validação contra os
casos da Etapa 02 em [`testes_casos.py`](testes_casos.py).

## Representação do estado

Na versão imperativa o estado eram estruturas soltas dentro de uma função:
`ordem`, `quantidades`, `linhas` e um dicionário `totais` com três
acumuladores. Todas viviam em `apurar`, e a corretude dependia de as quatro
serem atualizadas na ordem certa.

Na versão orientada a objetos o estado passou a morar **dentro dos objetos que
o representam**, e mudou de natureza em dois pontos:

- **O valor monetário virou um tipo.** Na versão imperativa todo valor era um
  inteiro de centavos circulando solto, e qualquer função podia somar dois
  números que não eram dinheiro. Agora existe `Dinheiro`, que guarda os
  centavos e não os expõe: quem usa soma, multiplica e formata, sem saber da
  representação.
- **Os acumuladores desapareceram.** `Apuracao` não guarda subtotal, descontos
  e total: ela **deriva** os três das linhas que a compõem. Não existe mais a
  possibilidade de o total ficar fora de sincronia com as linhas, que na versão
  imperativa dependia de `acumular_totais` ser chamada em todas as voltas do
  laço.

`Linha` calcula bruto e desconto no construtor e não muda depois. O objeto
nasce pronto, em vez de nascer vazio e ser preenchido.

## Responsabilidades

A mudança mais visível. Na versão imperativa uma única função, `apurar`, sabia
tudo: validar, agrupar, escolher a fórmula da promoção e somar. As demais
funções eram auxiliares dela.

Agora cada classe responde por uma coisa:

| Classe | Responsabilidade |
|---|---|
| `Dinheiro` | aritmética monetária e arredondamento |
| `Promocao` e subclasses | quanto de desconto para uma quantidade |
| `Produto` | preço, descrição, e delegar o desconto à sua promoção |
| `Catalogo` | ser a fonte de preço e promoção; recusar código inexistente |
| `Carrinho` | validar lançamentos e agrupar por código |
| `Linha` | o resultado de um produto |
| `Apuracao` | as linhas e os totais derivados delas |

O arredondamento é um bom exemplo: na versão imperativa ele era a expressão
`(bruto * percentual + 50) // 100`, escrita no meio de `calcular_desconto`.
Agora é `Dinheiro.percentual`, e quem precisa de um percentual não precisa
saber como se arredonda.

## Relacionamento entre componentes

Só há **uma hierarquia de herança**: `Promocao` e suas quatro subclasses. Ela se
justifica porque as quatro são de fato o mesmo tipo de coisa — respondem à
mesma pergunta, com a mesma assinatura, e quem chama não precisa saber qual
delas está ali. É o que substitui o encadeamento de `if` sobre o primeiro
elemento da tupla, que era como a versão imperativa escolhia a fórmula.

Nos demais relacionamentos a **composição é mais adequada**, e foi o que usei:

- `Produto` **tem uma** `Promocao`. Um produto não é um tipo de promoção;
  herdar aqui seria forçar a herança só para cumprir o requisito.
- `Catalogo` **agrega** `Produto`. Os produtos existem independentemente do
  catálogo que os reúne.
- `Apuracao` **é composta de** `Linha`. As linhas não existem fora da apuração
  que as produziu.
- `Carrinho` usa um `Catalogo` recebido no construtor, em vez de alcançar uma
  variável global como a versão imperativa fazia.

`SemPromocao` merece nota: em vez de `Produto` verificar se a promoção é nula,
existe uma subclasse que devolve desconto zero. O caso "não tem promoção" deixou
de ser um `if` e virou mais um objeto da hierarquia.

## Reutilização

A reutilização não veio da herança, e sim da composição e do tipo `Dinheiro`.
As quatro subclasses de promoção não compartilham código entre si — só o
contrato — porque as fórmulas são genuinamente diferentes. O que se reutiliza é
`Dinheiro`, usado por todas elas, por `Produto`, por `Linha` e por `Apuracao`.

Na versão imperativa a "reutilização" era chamar a mesma função; aqui é usar o
mesmo tipo, com a garantia adicional de que ele não pode ser usado errado.

## Encapsulamento

Três pontos concretos:

- `Dinheiro` guarda `_centavos` e não oferece jeito de ler o inteiro. A decisão
  de representar dinheiro em centavos, que na versão imperativa estava espalhada
  por todo o módulo, agora está confinada a uma classe.
- As subclasses de `Promocao` guardam seus parâmetros (`_n`, `_m`, `_limiar`)
  como privados. Ninguém de fora inspeciona os parâmetros de uma promoção para
  decidir o que fazer: pergunta-se o desconto e pronto.
- `Apuracao` devolve `linhas` como tupla, não como a lista interna, de modo que
  quem recebe não consegue alterar a apuração por fora.

`LeveNPagueM` também valida o próprio estado no construtor (`0 < m < n`): um
objeto inválido não chega a existir. Na versão imperativa a tupla
`("leve_n_pague_m", 3, 2)` podia ser montada errada e só falharia no cálculo.

## Extensão do sistema

É onde a diferença fica mais clara. Acrescentar um quarto tipo de promoção:

- **Na versão imperativa**, seria preciso abrir `calcular_desconto`,
  acrescentar mais um ramo ao encadeamento de `if`, e abrir também
  `descrever_promocao` para acrescentar outro ramo. Duas funções existentes
  mudam.
- **Na versão orientada a objetos**, escreve-se uma classe nova que herda de
  `Promocao` e implementa `desconto` e `__str__`. **Nenhum código existente é
  tocado** — nem `Produto`, nem `Linha`, nem `Apuracao`.

Em compensação, mudar o contrato é mais caro aqui: se `desconto` passasse a
receber um argumento a mais, as quatro subclasses teriam de mudar, enquanto na
versão imperativa havia uma função só. A orientação a objetos facilitou
acrescentar casos e dificultou mudar a operação — que é exatamente a troca que
o paradigma propõe.

## Validação

Os 15 casos da Etapa 02 passam nesta implementação
([`../testes/casos.md`](../testes/casos.md)):

```
$ python testes_casos.py
...
15 casos: 15 aprovados, 0 reprovados
```

As duas implementações também foram comparadas diretamente em 4.000 carrinhos
aleatórios, sem divergência de subtotal, descontos ou total — o que confirma
que a mudança foi de modelagem, e não de comportamento.
