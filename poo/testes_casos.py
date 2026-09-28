# -*- coding: utf-8 -*-
"""
Validação da implementação orientada a objetos contra os casos da Etapa 02
(testes/casos.md). São os mesmos 15 casos usados na versão imperativa.

Execução:  python testes_casos.py
"""

from caixa import (Carrinho, catalogo_de_referencia,
                   ProdutoInexistente, QuantidadeInvalida)

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

LINHAS_ESPERADAS = {"N10": [("CAFE", 3), ("ARROZ", 4), ("FEIJAO", 1)], "F01": []}


def main():
    aprovados = reprovados = 0

    for identificador, lancamentos, esperado in CASOS:
        carrinho = Carrinho(catalogo_de_referencia())
        try:
            for codigo, quantidade in lancamentos:
                carrinho.lancar(codigo, quantidade)
            apuracao = carrinho.apurar()
            erro = None
        except (ProdutoInexistente, QuantidadeInvalida) as e:
            apuracao, erro = None, str(e)

        if esperado == "erro":
            passou = erro is not None
            obtido = erro or "sem erro"
        elif erro is not None:
            passou, obtido = False, "ERRO: " + erro
        else:
            tupla = (str(apuracao.subtotal), str(apuracao.descontos),
                     str(apuracao.total))
            passou = tupla == esperado
            obtido = "subtotal %s | descontos %s | total %s" % tupla
            if identificador in LINHAS_ESPERADAS:
                linhas = [(l.codigo, l.quantidade) for l in apuracao.linhas]
                if linhas != LINHAS_ESPERADAS[identificador]:
                    passou = False
                    obtido += "  LINHAS: %s" % linhas

        if passou:
            aprovados += 1
        else:
            reprovados += 1
        print("%s %s  %s" % ("ok    " if passou else "FALHOU",
                             identificador, obtido))
        if not passou and esperado != "erro":
            print("         esperado: subtotal %s | descontos %s | total %s"
                  % esperado)

    print()
    print("%d casos: %d aprovados, %d reprovados"
          % (len(CASOS), aprovados, reprovados))


if __name__ == "__main__":
    main()
