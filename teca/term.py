# coding: utf-8


"""Módulo para operações comuns de entrada/saída no terminal.
"""


def imprimir_tabela(tabela):
    """Imprime todas as tuplas da tabela"""
    tuplas = tabela.select_all()
    for tupla in tuplas:
        print("======================")
        print(tupla)
    print("======================")


def menu_enumeracao(opcoes):
    """Constroi um menu de enumeração como pergunta."""
    for escolha, item in opcoes.items():
        print(f'{escolha}. {item.upper()}')
    while True:
        op = input('>>> ')
        if op in opcoes:
            break
        else:
            print('Opção inválida')

    return op
