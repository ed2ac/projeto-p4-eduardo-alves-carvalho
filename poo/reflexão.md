# [P4-ETAPA-04] Implementação orientada a objetos

**Aluno:** Eduardo Alves Carvalho — 20241002803320

Como meu modelo mudou ao passar do paradigma imperativo para o orientado a
objetos. A implementação está em [`caixa.py`](caixa.py) e os testes em
[`testes_casos.py`](testes_casos.py).

## Representação do estado

Na versão imperativa o estado eram variáveis soltas dentro de `apurar`
(`linhas`, `subtotal`, `descontos`). Agora cada dado fica no objeto a que
pertence: o `Carrinho` guarda seus itens, a `Linha` guarda bruto, desconto e
líquido, e a `Apuracao` guarda as linhas e calcula os totais a partir delas.

## Responsabilidades

| Classe | Responsabilidade |
|---|---|
| `Promocao` e subclasses | calcular o desconto para uma quantidade |
| `Produto` | guardar código, descrição e preço, e pedir o desconto à sua promoção |
| `Catalogo` | encontrar um produto pelo código |
| `Carrinho` | receber os itens, validar e apurar |
| `Linha` | o resultado de um produto |
| `Apuracao` | as linhas, os totais e a impressão |

## Relacionamento entre componentes

Usei herança só nas promoções: `LevePague`, `PercentualAcimaDe` e `Pacote`
herdam de `Promocao` e cada uma implementa `desconto` do seu jeito
(polimorfismo). No resto usei composição, porque não faria sentido herdar: o
`Produto` tem uma promoção, o `Catalogo` tem produtos, o `Carrinho` usa um
catálogo e a `Apuracao` é formada por linhas.

## Reutilização

As subclasses de `Promocao` reaproveitam o mesmo contrato (o método
`desconto`), e o `Produto` usa qualquer uma delas sem saber qual é. A função
`formatar` é a mesma da versão imperativa.

## Encapsulamento

O `Catalogo` e o `Carrinho` guardam seus dados em atributos internos
(`_produtos`, `_itens`) e só se mexe neles pelos métodos `buscar` e
`adicionar`. Assim a validação do item acontece sempre que algo entra no
carrinho.

## Extensão do sistema

Para criar um novo tipo de promoção basta escrever uma nova subclasse de
`Promocao` com o método `desconto`. Na versão imperativa seria preciso mexer no
`if` de `calcular_desconto`.

## Validação

```
$ python testes_casos.py
...
15 de 15 casos aprovados
```
