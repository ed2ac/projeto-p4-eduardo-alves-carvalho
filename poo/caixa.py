# [P4-ETAPA-04] Implementação orientada a objetos
# Fechamento de compra com promoções, conforme docs/problema.md.
# Valores em centavos (inteiros), como na versão imperativa.

from abc import ABC, abstractmethod


def formatar(centavos):
    return "%d,%02d" % (centavos // 100, centavos % 100)


# Única hierarquia com herança: todas as promoções respondem à mesma
# pergunta (qual o desconto para esta quantidade), cada uma do seu jeito.
class Promocao(ABC):
    @abstractmethod
    def desconto(self, quantidade, preco):
        pass


class LevePague(Promocao):
    def __init__(self, leve, pague):
        self.leve = leve
        self.pague = pague

    def desconto(self, quantidade, preco):
        grupos = quantidade // self.leve
        cobradas = grupos * self.pague + (quantidade - grupos * self.leve)
        return (quantidade - cobradas) * preco


class PercentualAcimaDe(Promocao):
    def __init__(self, minimo, percentual):
        self.minimo = minimo
        self.percentual = percentual

    def desconto(self, quantidade, preco):
        if quantidade < self.minimo:
            return 0
        return (quantidade * preco * self.percentual + 50) // 100   # R8


class Pacote(Promocao):
    def __init__(self, unidades, valor):
        self.unidades = unidades
        self.valor = valor

    def desconto(self, quantidade, preco):
        pacotes = quantidade // self.unidades
        sobra = quantidade - pacotes * self.unidades
        return quantidade * preco - (pacotes * self.valor + sobra * preco)


# Produto TEM uma promoção (composição), não É uma promoção.
class Produto:
    def __init__(self, codigo, descricao, preco, promocao=None):
        self.codigo = codigo
        self.descricao = descricao
        self.preco = preco
        self.promocao = promocao

    def desconto(self, quantidade):
        if self.promocao is None:
            return 0
        return self.promocao.desconto(quantidade, self.preco)


class Catalogo:
    def __init__(self, produtos):
        self._produtos = {}
        for produto in produtos:
            self._produtos[produto.codigo] = produto

    def buscar(self, codigo):
        if codigo not in self._produtos:
            raise ValueError("codigo %s nao existe no catalogo" % codigo)
        return self._produtos[codigo]


class Carrinho:
    def __init__(self, catalogo):
        self._catalogo = catalogo
        self._itens = []

    def adicionar(self, codigo, quantidade):
        self._catalogo.buscar(codigo)
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("quantidade de %s deve ser um inteiro maior que zero" % codigo)
        self._itens.append((codigo, quantidade))

    def apurar(self):
        # soma as quantidades do mesmo codigo, mantendo a ordem em que apareceram
        ordem = []
        quantidades = {}
        for codigo, quantidade in self._itens:
            if codigo not in quantidades:
                ordem.append(codigo)
                quantidades[codigo] = 0
            quantidades[codigo] += quantidade

        linhas = []
        for codigo in ordem:
            linhas.append(Linha(self._catalogo.buscar(codigo), quantidades[codigo]))
        return Apuracao(linhas)


class Linha:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
        self.bruto = quantidade * produto.preco
        self.desconto = produto.desconto(quantidade)
        self.liquido = self.bruto - self.desconto


class Apuracao:
    def __init__(self, linhas):
        self.linhas = linhas
        self.subtotal = sum(linha.bruto for linha in linhas)
        self.descontos = sum(linha.desconto for linha in linhas)
        self.total = self.subtotal - self.descontos

    def imprimir(self):
        for linha in self.linhas:
            print("%-7s %-20s %3d  bruto %8s  desconto %7s  liquido %8s"
                  % (linha.produto.codigo, linha.produto.descricao, linha.quantidade,
                     formatar(linha.bruto), formatar(linha.desconto), formatar(linha.liquido)))
        print("Subtotal: ", formatar(self.subtotal))
        print("Descontos:", formatar(self.descontos))
        print("Total:    ", formatar(self.total))


def catalogo_de_referencia():
    return Catalogo([
        Produto("CAFE", "Cafe torrado 500 g", 1800, LevePague(3, 2)),
        Produto("ARROZ", "Arroz tipo 1, 5 kg", 2450, PercentualAcimaDe(4, 10)),
        Produto("FEIJAO", "Feijao carioca 1 kg", 800),
        Produto("SABAO", "Sabao em po 1 kg", 1200, Pacote(2, 2000)),
        Produto("SUCO", "Suco de uva 1 L", 799, PercentualAcimaDe(3, 10)),
    ])


if __name__ == "__main__":
    carrinho = Carrinho(catalogo_de_referencia())
    carrinho.adicionar("CAFE", 2)
    carrinho.adicionar("ARROZ", 4)
    carrinho.adicionar("FEIJAO", 1)
    carrinho.adicionar("CAFE", 1)
    carrinho.apurar().imprimir()
