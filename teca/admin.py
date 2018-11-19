# coding: utf-8

from teca import database
from teca import term
from teca import check
import getpass
from mysql.connector.errors import DatabaseError


def admin_ler_entrada(atributo):
    if atributo == 'senha_hash':
        valor = getpass.getpass(prompt="senha: ")
    elif 'data' in atributo:
        valor = check.entrada('>>> ', check.data)
    elif atributo == 'nickname':
        valor = check.entrada('>>> ', check.nickname)
    elif atributo == 'numero':
        valor = check.entrada('>>> ', check.telefone)
    else:
        valor = check.entrada('>>> ', check.nao_vazia)

    return valor


def escolher_tabela():
    print("Escolha uma das tabelas: ")
    tabelas = {str(idx+1): tabela
               for idx, tabela in enumerate(database.tabelas)}
    menu = {k: v._table for k, v in tabelas.items()}
    escolha = term.menu_enumeracao(menu)
    return tabelas[escolha]


def escolher_tupla(tabela):
    term.imprimir_tabela(tabela)
    print("Escolha a tupla: ")
    chave = []
    for atributo in tabela._primary_key:
        print("{}: ".format(atributo))
        valor = admin_ler_entrada(atributo)
        chave.append(valor)

    instancia = tabela.select(chave)
    return instancia


def admin_inserir():
    print("== INSERIR")
    tabela_escolhida = escolher_tabela()
    atributos = []
    print("Inserção dos atributos na tabela: ", tabela_escolhida._table)
    for nome_atributo in tabela_escolhida._columns:
        print(f'{nome_atributo}: ')
        entrada = admin_ler_entrada(nome_atributo)
        atributos.append(entrada)

    instancia = tabela_escolhida(*atributos)
    try:
        instancia.insert()
    except DatabaseError as e:
        print("Não foi possível completar a ação. Uma exceção foi disparada!")
        print("Exceção: ", e)


def admin_alterar():
    print("== ALTERAR")
    tabela_escolhida = escolher_tabela()
    instancia = escolher_tupla(tabela_escolhida)
    atributos = {str(idx+1): attr
                 for idx, attr in enumerate(tabela_escolhida._columns)}
    print("Escolha o atributo: ")
    escolha = term.menu_enumeracao(atributos)
    atributo_escolhido = atributos[escolha]
    print(f'Novo {atributo_escolhido}: ')
    novo_valor = admin_ler_entrada(atributo_escolhido)
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
