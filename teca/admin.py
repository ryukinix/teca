# coding: utf-8

from teca import database
from teca import term
import getpass

def escolher_tabela():
    print("Escolha uma das tabelas: ")
    dic = {idx+1: tabela for idx, tabela in enumerate(database.tabelas)}
    # equivalente:
    # dic = {}
    # for idx, tabela in enumerate(database.tabelas):
    #     dic[idx+1] = tabela
    for i, tabela in dic.items():
        print("{}. {}".format(i, tabela._table))

    # escolha da tabela
    while True:
        escolha = int(input(">>> "))
        if escolha in dic:
            break
        else:
            print("Escolha inválida!")

    return dic[escolha]


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
    atributos = {idx+1: att for idx, att in enumerate(tabela_escolhida._columns)}
    print("Escolha o atributo: ")
    for idx, attr in atributos.items():
        print(f"{idx}. {attr}")

    while True:
        escolha = int(input(">>> "))
        if escolha in atributos:
            break

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
    opcoes = [
        'Inserir',
        'Remover',
        'Alterar'
    ]
    print("Opções: ")
    for i, op in enumerate(opcoes):
        print("{}. {}".format(i+1, op))

    while True:
        opcao = int(input(">>> "))
        if opcao in range(1, len(opcoes) + 1):
            break

    if opcao == 1:
        admin_inserir()
    elif opcao == 2:
        admin_remover()
    elif opcao == 3:
        admin_alterar()
