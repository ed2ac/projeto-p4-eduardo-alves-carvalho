# -*- coding: utf-8 -*-
"""
Validação da implementação imperativa contra os casos da Etapa 02
(testes/casos.md).

Execução:  python testes_casos.py
"""

from caixa import CATALOGO, apurar, formatar

# Cada caso: identificador, carrinho, resultado esperado.
# Para carrinho válido o esperado é (subtotal, descontos, total) em texto.
# Para carrinho inválido o esperado é a palavra "erro".
CASOS = [
    ("N01", [("FEIJAO", 2)],                              ("16,00", "0,00", "16,00")),
    ("N02", [("FEIJAO", 1)],                              ("8,00", "0,00", "8,00")),
    ("N03", [("CAFE", 3)],                                ("54,00", "18,00", "36,00")),
    ("N04", [("CAFE", 5)],                                ("90,00", "18,00", "72,00")),
    ("N05", [("CAFE", 6)],                                ("108,00", "36,00", "72,00")),
    ("N06", [("ARROZ", 4)],                               ("98,00", "9,80", "88,20")),
    ("N07", [("ARROZ", 6)],                               ("147,00", "14,70", "132,30")),
    ("N08", [("SABAO", 4)],                               ("48,00", "8,00", "40,00")),
    ("N09", [("SABAO", 5)],                               ("60,00", "8,00", "52,00")),
    ("N10", [("CAFE", 2), ("ARROZ", 4),
             ("FEIJAO", 1), ("CAFE", 1)],                 ("160,00", "27,80", "132,20")),
    ("F01", [],                                           ("0,00", "0,00", "0,00")),
    ("F02", [("ARROZ", 3)],                               ("73,50", "0,00", "73,50")),
    ("F03", [("SUCO", 3)],                                ("23,97", "2,40", "21,57")),
    ("X01", [("CAFE", 2), ("BISCOITO", 1)],               "erro"),
    ("X02", [("FEIJAO", 0)],                              "erro"),
]

# Linhas esperadas nos casos em que o carrinho tem mais de um produto ou
# agregação de códigos repetidos, para conferir também R1 e R2.
LINHAS_ESPERADAS = {
    "N10": [("CAFE", 3), ("ARROZ", 4), ("FEIJAO", 1)],
    "F01": [],
}


def main():
    aprovados = 0
    reprovados = 0

    for identificador, carrinho, esperado in CASOS:
        resultado = apurar(carrinho, CATALOGO)

        if esperado == "erro":
            passou = resultado["erro"] is not None
            obtido = resultado["erro"] if resultado["erro"] else "sem erro"
        else:
            if resultado["erro"] is not None:
                passou = False
                obtido = "ERRO: " + resultado["erro"]
            else:
                totais = resultado["totais"]
                obtido_tupla = (formatar(totais["subtotal"]),
                                formatar(totais["descontos"]),
                                formatar(totais["total"]))
                passou = obtido_tupla == esperado
                obtido = "subtotal %s | descontos %s | total %s" % obtido_tupla

                # confere quantidade e ordem das linhas, quando especificado
                if identificador in LINHAS_ESPERADAS:
                    linhas = [(l["codigo"], l["quantidade"])
                              for l in resultado["linhas"]]
                    if linhas != LINHAS_ESPERADAS[identificador]:
                        passou = False
                        obtido = obtido + "  LINHAS: %s" % linhas

        if passou:
            aprovados = aprovados + 1
            marca = "ok    "
        else:
            reprovados = reprovados + 1
            marca = "FALHOU"

        print("%s %s  %s" % (marca, identificador, obtido))
        if not passou and esperado != "erro":
            print("         esperado: subtotal %s | descontos %s | total %s"
                  % esperado)

    print()
    print("%d casos: %d aprovados, %d reprovados"
          % (len(CASOS), aprovados, reprovados))


if __name__ == "__main__":
    main()
