# coding: utf-8


"""Módulo para operações comuns de entrada/saída no terminal.
"""

from tabulate import tabulate
from teca import database


def imprimir_tabela(tabela):
    """Imprime todas as tuplas da tabela"""
    tuples = tabela.select_all()
    if tabela == database.Usuario:
        for u in tuples:
            u.senha_hash = '***SECRET***'

    rows = [list(row) for row in tuples]
    print(tabulate(rows, tabela._columns, 'psql'))


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
