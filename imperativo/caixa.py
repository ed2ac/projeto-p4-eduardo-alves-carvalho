# -*- coding: utf-8 -*-
"""
[P4-ETAPA-03] Implementação imperativa

Fechamento de compra com promoções, conforme docs/problema.md.

Os valores monetários são tratados como números inteiros de centavos. Isso
evita os erros de arredondamento do ponto flutuante e deixa a regra R8
(arredondamento do desconto, meio para cima) escrita com divisão inteira.
"""

# --------------------------------------------------------------------------
# Catálogo de referência (seção 3.3 da especificação).
# Os preços estão em centavos. A promoção é uma tupla cujo primeiro elemento
# diz o tipo, ou None quando o produto não tem promoção.
# --------------------------------------------------------------------------
CATALOGO = {
    "CAFE":   {"descricao": "Cafe torrado 500 g",
               "preco": 1800, "promocao": ("leve_n_pague_m", 3, 2)},
    "ARROZ":  {"descricao": "Arroz tipo 1, 5 kg",
               "preco": 2450, "promocao": ("percentual_acima_de", 4, 10)},
    "FEIJAO": {"descricao": "Feijao carioca 1 kg",
               "preco": 800,  "promocao": None},
    "SABAO":  {"descricao": "Sabao em po 1 kg",
               "preco": 1200, "promocao": ("pacote", 2, 2000)},
    "SUCO":   {"descricao": "Suco de uva 1 L",
               "preco": 799,  "promocao": ("percentual_acima_de", 3, 10)},
}


def formatar(centavos):
    """Converte centavos em texto com duas casas decimais."""
    return "%d,%02d" % (centavos // 100, centavos % 100)


def descrever_promocao(promocao):
    """Texto da promoção, para aparecer na linha do comprovante."""
    if promocao is None:
        return "sem promocao"

    tipo = promocao[0]
    if tipo == "leve_n_pague_m":
        return "leve %d pague %d" % (promocao[1], promocao[2])
    if tipo == "percentual_acima_de":
        return "%d%% a partir de %d un" % (promocao[2], promocao[1])
    if tipo == "pacote":
        return "%d por %s" % (promocao[1], formatar(promocao[2]))
    return "promocao desconhecida"


def validar_carrinho(carrinho, catalogo):
    """Percorre o carrinho e devolve a mensagem do primeiro problema, ou None.

    A varredura para no primeiro erro porque, pela R10, basta um item inválido
    para o carrinho inteiro ser recusado.
    """
    posicao = 0
    while posicao < len(carrinho):
        codigo, quantidade = carrinho[posicao]

        if codigo not in catalogo:
            return "codigo '%s' nao existe no catalogo" % codigo

        # bool é subtipo de int em Python, então precisa ser descartado aqui
        if isinstance(quantidade, bool) or not isinstance(quantidade, int):
            return "quantidade de '%s' nao e um numero inteiro" % codigo
        if quantidade <= 0:
            return "quantidade de '%s' deve ser maior que zero" % codigo

        posicao = posicao + 1

    return None


def agregar_itens(carrinho):
    """Soma as quantidades por código (R1) preservando a ordem de entrada (R2).

    Mantém duas estruturas que vão sendo modificadas a cada volta do laço:
    `ordem`, que registra a primeira aparição de cada código, e `quantidades`,
    que acumula o total por código.
    """
    ordem = []
    quantidades = {}

    for codigo, quantidade in carrinho:
        if codigo not in quantidades:
            ordem.append(codigo)
            quantidades[codigo] = 0
        quantidades[codigo] = quantidades[codigo] + quantidade

    return ordem, quantidades


def calcular_desconto(promocao, quantidade, preco):
    """Desconto da linha, em centavos, conforme as regras R4 a R8."""
    if promocao is None:
        return 0

    bruto = quantidade * preco
    tipo = promocao[0]

    if tipo == "leve_n_pague_m":
        n = promocao[1]
        m = promocao[2]
        grupos = quantidade // n
        unidades_cobradas = grupos * m + (quantidade - grupos * n)
        return bruto - unidades_cobradas * preco

    if tipo == "percentual_acima_de":
        limiar = promocao[1]
        percentual = promocao[2]
        if quantidade < limiar:
            return 0
        # R8: arredondamento meio para cima, feito com divisão inteira
        return (bruto * percentual + 50) // 100

    if tipo == "pacote":
        k = promocao[1]
        valor = promocao[2]
        pacotes = quantidade // k
        sobra = quantidade - pacotes * k
        return bruto - (pacotes * valor + sobra * preco)

    return 0


def acumular_totais(totais, bruto, desconto):
    """Soma os valores de uma linha nos totais da apuração.

    Este subprograma existe para concentrar a atualização dos acumuladores em
    um lugar só. Ele MODIFICA o dicionário recebido por parâmetro, em vez de
    devolver um novo: é um efeito colateral deliberado.
    """
    totais["subtotal"] = totais["subtotal"] + bruto
    totais["descontos"] = totais["descontos"] + desconto
    totais["total"] = totais["total"] + (bruto - desconto)


def apurar(carrinho, catalogo):
    """Apura o carrinho e devolve o resultado.

    Fluxo: validar, agregar, calcular linha a linha, acumular totais.
    """
    erro = validar_carrinho(carrinho, catalogo)
    if erro is not None:
        return {"erro": erro, "linhas": [], "totais": None}

    ordem, quantidades = agregar_itens(carrinho)

    linhas = []
    totais = {"subtotal": 0, "descontos": 0, "total": 0}

    for codigo in ordem:
        produto = catalogo[codigo]
        quantidade = quantidades[codigo]
        preco = produto["preco"]

        bruto = quantidade * preco
        desconto = calcular_desconto(produto["promocao"], quantidade, preco)
        liquido = bruto - desconto

        linhas.append({
            "codigo": codigo,
            "descricao": produto["descricao"],
            "quantidade": quantidade,
            "bruto": bruto,
            "desconto": desconto,
            "promocao": descrever_promocao(produto["promocao"]),
            "liquido": liquido,
        })

        acumular_totais(totais, bruto, desconto)

    return {"erro": None, "linhas": linhas, "totais": totais}


def imprimir_apuracao(resultado):
    """Escreve o resultado na saída padrão."""
    if resultado["erro"] is not None:
        print("CARRINHO RECUSADO: %s" % resultado["erro"])
        return

    print("%-8s %-22s %4s %10s %10s %10s  %s"
          % ("CODIGO", "DESCRICAO", "QTD", "BRUTO", "DESCONTO",
             "LIQUIDO", "PROMOCAO"))

    for linha in resultado["linhas"]:
        print("%-8s %-22s %4d %10s %10s %10s  %s"
              % (linha["codigo"], linha["descricao"], linha["quantidade"],
                 formatar(linha["bruto"]), formatar(linha["desconto"]),
                 formatar(linha["liquido"]), linha["promocao"]))

    totais = resultado["totais"]
    print("-" * 78)
    print("Subtotal  %s" % formatar(totais["subtotal"]))
    print("Descontos %s" % formatar(totais["descontos"]))
    print("TOTAL     %s" % formatar(totais["total"]))


def main():
    """Roda o exemplo E5 da especificação."""
    carrinho = [("CAFE", 2), ("ARROZ", 4), ("FEIJAO", 1), ("CAFE", 1)]

    print("Carrinho:")
    for codigo, quantidade in carrinho:
        print("  %s x %d" % (codigo, quantidade))
    print()

    resultado = apurar(carrinho, CATALOGO)
    imprimir_apuracao(resultado)


if __name__ == "__main__":
    main()
