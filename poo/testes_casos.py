# Roda os 15 casos da Etapa 02 (testes/casos.md) na versao orientada a objetos.
# Execucao: python testes_casos.py

from caixa import Carrinho, catalogo_de_referencia, formatar

# (id, carrinho, (subtotal, descontos, total)) ou "erro"
CASOS = [
    ("N01", [("FEIJAO", 2)], ("16,00", "0,00", "16,00")),
    ("N02", [("FEIJAO", 1)], ("8,00", "0,00", "8,00")),
    ("N03", [("CAFE", 3)], ("54,00", "18,00", "36,00")),
    ("N04", [("CAFE", 5)], ("90,00", "18,00", "72,00")),
    ("N05", [("CAFE", 6)], ("108,00", "36,00", "72,00")),
    ("N06", [("ARROZ", 4)], ("98,00", "9,80", "88,20")),
    ("N07", [("ARROZ", 6)], ("147,00", "14,70", "132,30")),
    ("N08", [("SABAO", 4)], ("48,00", "8,00", "40,00")),
    ("N09", [("SABAO", 5)], ("60,00", "8,00", "52,00")),
    ("N10", [("CAFE", 2), ("ARROZ", 4), ("FEIJAO", 1), ("CAFE", 1)], ("160,00", "27,80", "132,20")),
    ("F01", [], ("0,00", "0,00", "0,00")),
    ("F02", [("ARROZ", 3)], ("73,50", "0,00", "73,50")),
    ("F03", [("SUCO", 3)], ("23,97", "2,40", "21,57")),
    ("X01", [("CAFE", 2), ("BISCOITO", 1)], "erro"),
    ("X02", [("FEIJAO", 0)], "erro"),
]

aprovados = 0
for id_caso, itens, esperado in CASOS:
    carrinho = Carrinho(catalogo_de_referencia())
    try:
        for codigo, quantidade in itens:
            carrinho.adicionar(codigo, quantidade)
        apuracao = carrinho.apurar()
        obtido = (formatar(apuracao.subtotal), formatar(apuracao.descontos), formatar(apuracao.total))
    except ValueError:
        obtido = "erro"

    if obtido == esperado:
        aprovados += 1
        print("ok     ", id_caso)
    else:
        print("FALHOU ", id_caso, "esperado", esperado, "obtido", obtido)

print("%d de %d casos aprovados" % (aprovados, len(CASOS)))
