# -*- coding: utf-8 -*-
"""
[P4-ETAPA-04] Implementação orientada a objetos

Fechamento de compra com promoções, conforme docs/problema.md.
"""

from abc import ABC, abstractmethod


class Dinheiro:
    """Valor monetário. Guarda centavos e não expõe a representação.

    Existe para que nenhuma outra classe precise saber que o valor é um inteiro
    de centavos: quem usa Dinheiro soma, multiplica e formata, sem tocar no
    número por dentro.
    """

    __slots__ = ("_centavos",)

    def __init__(self, centavos):
        self._centavos = int(centavos)

    @classmethod
    def de_reais(cls, reais, centavos=0):
        return cls(reais * 100 + centavos)

    def __add__(self, outro):
        return Dinheiro(self._centavos + outro._centavos)

    def __sub__(self, outro):
        return Dinheiro(self._centavos - outro._centavos)

    def vezes(self, n):
        return Dinheiro(self._centavos * n)

    def percentual(self, p):
        """p% deste valor, arredondado para o centavo mais próximo (meio para
        cima), como manda a regra R8."""
        return Dinheiro((self._centavos * p + 50) // 100)

    def __eq__(self, outro):
        return isinstance(outro, Dinheiro) and self._centavos == outro._centavos

    def __hash__(self):
        return hash(self._centavos)

    def __str__(self):
        return "%d,%02d" % (self._centavos // 100, self._centavos % 100)

    def __repr__(self):
        return "Dinheiro(%s)" % self


ZERO = Dinheiro(0)


# --------------------------------------------------------------------------
# Promoções: única hierarquia com herança no projeto.
# Todas respondem à mesma pergunta — quanto de desconto para esta quantidade
# deste preço — e a resposta muda por subclasse. É despacho dinâmico de fato,
# e não um rótulo verificado com if.
# --------------------------------------------------------------------------
class Promocao(ABC):

    @abstractmethod
    def desconto(self, quantidade, preco):
        """Desconto da linha, como Dinheiro."""

    @abstractmethod
    def __str__(self):
        """Texto da promoção, para o comprovante."""


class SemPromocao(Promocao):
    """Produto sem promoção. Evita que Produto precise tratar o caso nulo."""

    def desconto(self, quantidade, preco):
        return ZERO

    def __str__(self):
        return "sem promocao"


class LeveNPagueM(Promocao):

    def __init__(self, n, m):
        if not 0 < m < n:
            raise ValueError("leve n pague m exige 0 < m < n")
        self._n = n
        self._m = m

    def desconto(self, quantidade, preco):
        grupos = quantidade // self._n
        cobradas = grupos * self._m + (quantidade - grupos * self._n)
        return preco.vezes(quantidade) - preco.vezes(cobradas)

    def __str__(self):
        return "leve %d pague %d" % (self._n, self._m)


class PercentualAcimaDe(Promocao):

    def __init__(self, limiar, percentual):
        self._limiar = limiar
        self._percentual = percentual

    def desconto(self, quantidade, preco):
        if quantidade < self._limiar:
            return ZERO
        return preco.vezes(quantidade).percentual(self._percentual)

    def __str__(self):
        return "%d%% a partir de %d un" % (self._percentual, self._limiar)


class Pacote(Promocao):

    def __init__(self, unidades, valor):
        self._unidades = unidades
        self._valor = valor

    def desconto(self, quantidade, preco):
        pacotes = quantidade // self._unidades
        avulsas = quantidade - pacotes * self._unidades
        cobrado = self._valor.vezes(pacotes) + preco.vezes(avulsas)
        return preco.vezes(quantidade) - cobrado

    def __str__(self):
        return "%d por %s" % (self._unidades, self._valor)


# --------------------------------------------------------------------------
class ProdutoInexistente(Exception):
    pass


class QuantidadeInvalida(Exception):
    pass


class Produto:
    """Um produto do catálogo. Tem uma promoção por composição, não por
    herança: um produto não é um tipo de promoção, ele possui uma."""

    def __init__(self, codigo, descricao, preco, promocao=None):
        self._codigo = codigo
        self._descricao = descricao
        self._preco = preco
        self._promocao = promocao or SemPromocao()

    @property
    def codigo(self):
        return self._codigo

    @property
    def descricao(self):
        return self._descricao

    @property
    def promocao(self):
        return self._promocao

    def bruto(self, quantidade):
        return self._preco.vezes(quantidade)

    def desconto(self, quantidade):
        """Delega à promoção. O produto não sabe qual é o tipo dela."""
        return self._promocao.desconto(quantidade, self._preco)


class Catalogo:
    """Agrega produtos e é a única fonte de preço e promoção."""

    def __init__(self, produtos=()):
        self._produtos = {}
        for p in produtos:
            self.incluir(p)

    def incluir(self, produto):
        self._produtos[produto.codigo] = produto

    def buscar(self, codigo):
        if codigo not in self._produtos:
            raise ProdutoInexistente(
                "codigo '%s' nao existe no catalogo" % codigo)
        return self._produtos[codigo]


class Carrinho:
    """Sequência de lançamentos. Sabe validar e agrupar os próprios itens."""

    def __init__(self, catalogo):
        self._catalogo = catalogo
        self._lancamentos = []

    def lancar(self, codigo, quantidade):
        if isinstance(quantidade, bool) or not isinstance(quantidade, int):
            raise QuantidadeInvalida(
                "quantidade de '%s' nao e um numero inteiro" % codigo)
        if quantidade <= 0:
            raise QuantidadeInvalida(
                "quantidade de '%s' deve ser maior que zero" % codigo)
        self._catalogo.buscar(codigo)       # valida o codigo no lancamento
        self._lancamentos.append((codigo, quantidade))
        return self

    def agrupado(self):
        """Pares (produto, quantidade) na ordem da primeira citação."""
        ordem, soma = [], {}
        for codigo, quantidade in self._lancamentos:
            if codigo not in soma:
                ordem.append(codigo)
                soma[codigo] = 0
            soma[codigo] += quantidade
        return [(self._catalogo.buscar(c), soma[c]) for c in ordem]

    def apurar(self):
        return Apuracao([Linha(p, q) for p, q in self.agrupado()])


class Linha:
    """Resultado por produto. Calcula-se na construção e não muda depois."""

    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade
        self._bruto = produto.bruto(quantidade)
        self._desconto = produto.desconto(quantidade)

    @property
    def quantidade(self):
        return self._quantidade

    @property
    def bruto(self):
        return self._bruto

    @property
    def desconto(self):
        return self._desconto

    @property
    def liquido(self):
        return self._bruto - self._desconto

    @property
    def codigo(self):
        return self._produto.codigo

    def __str__(self):
        return "%-8s %-22s %4d %10s %10s %10s  %s" % (
            self._produto.codigo, self._produto.descricao, self._quantidade,
            self._bruto, self._desconto, self.liquido, self._produto.promocao)


class Apuracao:
    """Composta pelas linhas. Os totais são derivados delas, nunca guardados
    em paralelo: não existe estado que possa ficar fora de sincronia."""

    def __init__(self, linhas):
        self._linhas = list(linhas)

    @property
    def linhas(self):
        return tuple(self._linhas)

    @property
    def subtotal(self):
        total = ZERO
        for linha in self._linhas:
            total = total + linha.bruto
        return total

    @property
    def descontos(self):
        total = ZERO
        for linha in self._linhas:
            total = total + linha.desconto
        return total

    @property
    def total(self):
        return self.subtotal - self.descontos

    def __str__(self):
        cab = "%-8s %-22s %4s %10s %10s %10s  %s" % (
            "CODIGO", "DESCRICAO", "QTD", "BRUTO", "DESCONTO",
            "LIQUIDO", "PROMOCAO")
        corpo = [str(l) for l in self._linhas]
        rodape = ["-" * 78,
                  "Subtotal  %s" % self.subtotal,
                  "Descontos %s" % self.descontos,
                  "TOTAL     %s" % self.total]
        return "\n".join([cab] + corpo + rodape)


def catalogo_de_referencia():
    """Catálogo da seção 3.3 da especificação."""
    return Catalogo([
        Produto("CAFE", "Cafe torrado 500 g", Dinheiro.de_reais(18),
                LeveNPagueM(3, 2)),
        Produto("ARROZ", "Arroz tipo 1, 5 kg", Dinheiro.de_reais(24, 50),
                PercentualAcimaDe(4, 10)),
        Produto("FEIJAO", "Feijao carioca 1 kg", Dinheiro.de_reais(8)),
        Produto("SABAO", "Sabao em po 1 kg", Dinheiro.de_reais(12),
                Pacote(2, Dinheiro.de_reais(20))),
        Produto("SUCO", "Suco de uva 1 L", Dinheiro.de_reais(7, 99),
                PercentualAcimaDe(3, 10)),
    ])


def main():
    carrinho = Carrinho(catalogo_de_referencia())
    carrinho.lancar("CAFE", 2).lancar("ARROZ", 4) \
            .lancar("FEIJAO", 1).lancar("CAFE", 1)
    print(carrinho.apurar())


if __name__ == "__main__":
    main()
