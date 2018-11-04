# coding: utf-8

from teca import database
from teca import term
import getpass

def escolher_tabela():
    print("Escolha uma das tabelas: ")
    tabelas = {str(idx+1): tabela
               for idx, tabela in enumerate(database.tabelas)}
    menu = {k: v._table for k,v in tabelas.items()}
    escolha = term.menu_enumeracao(menu)
    return tabelas[escolha]


def escolher_tupla(tabela):
    term.imprimir_tabela(tabela)
    print("Escolha a tupla: ")
    chave = []
    for atributo in tabela._primary_key:
        valor = input("{}: ".format(atributo))
        chave.append(valor)

    instancia = tabela.select(chave)
    return instancia


def admin_inserir():
    print("== INSERIR")
    tabela_escolhida = escolher_tabela()
    # inserção dos campos
    atributos = []
    print("Inserção dos atributos na tabela: ", tabela_escolhida._table)
    for nome_atributo in tabela_escolhida._columns:
        entrada = input("{}: ".format(nome_atributo))
        atributos.append(entrada)

    instancia = tabela_escolhida(*atributos)
    instancia.insert()


def admin_inserir():
    print("== INSERIR")
    tabela_escolhida = escolher_tabela()
    # inserção dos campos
    atributos = []
    print("Inserção dos atributos na tabela: ", tabela_escolhida._table)
    for nome_atributo in tabela_escolhida._columns:
        entrada = input("{}: ".format(nome_atributo))
        atributos.append(entrada)

    instancia = tabela_escolhida(*atributos)
    instancia.insert()


def admin_alterar():
    print("== ALTERAR")
    tabela_escolhida = escolher_tabela()
    instancia = escolher_tupla(tabela_escolhida)
    atributos = {str(idx+1): attr
                 for idx, attr in enumerate(tabela_escolhida._columns)}
    print("Escolha o atributo: ")
    escolha = term.menu_enumeracao(atributos)
    atributo_escolhido = atributos[escolha]
    novo_valor = input(f"Novo {atributo_escolhido}: ",)
    setattr(instancia, atributo_escolhido, novo_valor)
    instancia.update()


def admin_remover():
    print("== REMOVER")
    tabela_escolhida = escolher_tabela()
    instancia = escolher_tupla(tabela_escolhida)
    instancia.delete()


def tela_admin():
    while True:
        opcoes = {
            '0': 'Sair',
            '1': 'Inserir',
            '2': 'Remover',
            '3': 'Alterar',
        }
        print("Opções: ")
        opcao = term.menu_enumeracao(opcoes)
        if opcao == '0':
            break
        elif opcao == '1':
            admin_inserir()
        elif opcao == '2':
            admin_remover()
        elif opcao == '3':
            admin_alterar()
