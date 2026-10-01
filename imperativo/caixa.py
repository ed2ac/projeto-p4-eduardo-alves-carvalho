# [P4-ETAPA-03] Implementação imperativa
# Fechamento de compra com promoções, conforme docs/problema.md.
# Os valores são guardados em centavos (inteiros) para evitar erro de
# arredondamento com números decimais.

# promocao: None ou uma tupla (tipo, parametro1, parametro2)
CATALOGO = {
    "CAFE":   {"descricao": "Cafe torrado 500 g",  "preco": 1800, "promocao": ("leve_pague", 3, 2)},
    "ARROZ":  {"descricao": "Arroz tipo 1, 5 kg",  "preco": 2450, "promocao": ("percentual", 4, 10)},
    "FEIJAO": {"descricao": "Feijao carioca 1 kg", "preco": 800,  "promocao": None},
    "SABAO":  {"descricao": "Sabao em po 1 kg",    "preco": 1200, "promocao": ("pacote", 2, 2000)},
    "SUCO":   {"descricao": "Suco de uva 1 L",     "preco": 799,  "promocao": ("percentual", 3, 10)},
}


def formatar(centavos):
    return "%d,%02d" % (centavos // 100, centavos % 100)


def validar(carrinho, catalogo):
    # devolve a mensagem do primeiro erro, ou None se o carrinho estiver certo
    for codigo, quantidade in carrinho:
        if codigo not in catalogo:
            return "codigo %s nao existe no catalogo" % codigo
        if not isinstance(quantidade, int) or quantidade <= 0:
            return "quantidade de %s deve ser um inteiro maior que zero" % codigo
    return None


def agrupar(carrinho):
    # soma as quantidades do mesmo codigo, mantendo a ordem em que apareceram
    ordem = []
    quantidades = {}
    for codigo, quantidade in carrinho:
        if codigo not in quantidades:
            ordem.append(codigo)
            quantidades[codigo] = 0
        quantidades[codigo] = quantidades[codigo] + quantidade
    return ordem, quantidades


def calcular_desconto(promocao, quantidade, preco):
    if promocao is None:
        return 0

    tipo, a, b = promocao
    bruto = quantidade * preco

    if tipo == "leve_pague":        # leve a pague b
        grupos = quantidade // a
        cobradas = grupos * b + (quantidade - grupos * a)
        return bruto - cobradas * preco

    if tipo == "percentual":        # b% a partir de a unidades
        if quantidade < a:
            return 0
        return (bruto * b + 50) // 100    # +50 arredonda meio para cima (R8)

    if tipo == "pacote":            # a unidades por b centavos
        pacotes = quantidade // a
        sobra = quantidade - pacotes * a
        return bruto - (pacotes * b + sobra * preco)

    return 0


def apurar(carrinho, catalogo):
    erro = validar(carrinho, catalogo)
    if erro is not None:
        return erro, [], 0, 0

    ordem, quantidades = agrupar(carrinho)

    linhas = []
    subtotal = 0
    descontos = 0

    for codigo in ordem:
        produto = catalogo[codigo]
        quantidade = quantidades[codigo]
        bruto = quantidade * produto["preco"]
        desconto = calcular_desconto(produto["promocao"], quantidade, produto["preco"])

        linhas.append((codigo, produto["descricao"], quantidade, bruto, desconto))
        subtotal = subtotal + bruto
        descontos = descontos + desconto

    return None, linhas, subtotal, descontos


def imprimir(erro, linhas, subtotal, descontos):
    if erro is not None:
        print("Carrinho recusado:", erro)
        return

    for codigo, descricao, quantidade, bruto, desconto in linhas:
        print("%-7s %-20s %3d  bruto %8s  desconto %7s  liquido %8s"
              % (codigo, descricao, quantidade, formatar(bruto),
                 formatar(desconto), formatar(bruto - desconto)))
    print("Subtotal: ", formatar(subtotal))
    print("Descontos:", formatar(descontos))
    print("Total:    ", formatar(subtotal - descontos))


if __name__ == "__main__":
    carrinho = [("CAFE", 2), ("ARROZ", 4), ("FEIJAO", 1), ("CAFE", 1)]
    erro, linhas, subtotal, descontos = apurar(carrinho, CATALOGO)
    imprimir(erro, linhas, subtotal, descontos)
