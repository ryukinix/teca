# coding: utf-8

from teca import database
from teca import term
from teca import check
import getpass
from mysql.connector.errors import DatabaseError


def admin_ler_entrada(atributo):
    if atributo == 'senha_hash':
        valor = database.senha_hash(getpass.getpass(prompt="senha: "))
    elif 'data' in atributo:
        valor = check.entrada('>>> ', check.data)
    elif atributo == 'nickname':
        valor = check.entrada('>>> ', check.nickname)
    elif atributo == 'numero':
        valor = check.entrada('>>> ', check.telefone)
    elif 'cpf' in atributo:
        valor = check.entrada('>>> ', check.cpf)
    elif 'isbn' in atributo:
        valor = check.entrada('>>> ', check.isnb)
    else:
        valor = check.entrada('>>> ', check.nao_vazia)

    return valor


def escolher_tabela(t):
    print("Escolha uma das tabelas: ")
    tabelas = {str(idx+1): tabela
               for idx, tabela in enumerate(t)}
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
    tabela_escolhida = escolher_tabela(database.tabelas_sem_isa)
    atributos = []
    print("Inserção dos atributos na tabela: ", tabela_escolhida._table)
    for nome_atributo in tabela_escolhida._columns:
        if nome_atributo != 'senha_hash':
            print(f'{nome_atributo}: ')
        entrada = admin_ler_entrada(nome_atributo)
        atributos.append(entrada)

    instancia = tabela_escolhida(*atributos)

    if tabela_escolhida._table == 'usuario':
        if instancia.tipo == 'aluno':
            tabela = database.Aluno
        elif instancia.tipo == 'funcionario':
            tabela = database.Funcionario
        elif instancia.tipo == 'professor':
            tabela = database.Professor
        else:
            print("Tipo de usuário inválido!")
            return
        atributos = [instancia.matricula]
        print("Inserção dos atributos na tabela: ", tabela._table)
        for nome_atributo in tabela._columns[1:]:
            print(f'{nome_atributo}: ')
            entrada = admin_ler_entrada(nome_atributo)
            atributos.append(entrada)

        usuario_extra = tabela(*atributos)

    try:
        status = instancia.insert()
        if tabela_escolhida._table == 'usuario' and status:
            usuario_extra.insert()
    except DatabaseError as e:
        print("Não foi possível completar a ação. Uma exceção foi disparada!")
        print("Exceção: ", e)
        if status:
            instancia.delete()
        return

    if status:
        print("INSERÇÃO FINALIZADA COM SUCESSO!")


def admin_alterar():
    print("== ALTERAR")
    tabela_escolhida = escolher_tabela(database.tabelas_todas)
    colunas = [k for k in tabela_escolhida._columns
               if k not in tabela_escolhida._primary_key]
    instancia = escolher_tupla(tabela_escolhida)
    atributos = {str(idx+1): attr
                 for idx, attr in enumerate(colunas)}
    print("Escolha o atributo: ")
    escolha = term.menu_enumeracao(atributos)
    atributo_escolhido = atributos[escolha]
    print(f'Novo {atributo_escolhido}: ')
    novo_valor = admin_ler_entrada(atributo_escolhido)
    setattr(instancia, atributo_escolhido, novo_valor)
    if instancia is not None:
        updated = instancia.update()
        if updated:
            print("TUPLA ATUALIZADA COM SUCESSO!")
    else:
        print("TUPLA NÃO ENCONTRADA.")


def admin_remover():
    print("== REMOVER")
    tabela_escolhida = escolher_tabela(database.tabelas_sem_isa)
    instancia = escolher_tupla(tabela_escolhida)
    if instancia is not None:
        deleted = instancia.delete()
        if deleted:
            print("TUPLA DELETADA COM SUCESSO!")
    else:
        print("TUPLA NÃO ENCONTRADA.")


def admin_imprimir():
    print("== IMPRIMIR")
    tabela_escolhida = escolher_tabela(database.tabelas_todas)
    term.imprimir_tabela(tabela_escolhida)


def tela_admin():
    print("== TELA DE ADMINISTRADOR ==")
    while True:
        opcoes = {
            '1': 'Inserir',
            '2': 'Remover',
            '3': 'Alterar',
            '4': 'Consultar',
        }
        print("Opções: ")
        opcao = term.menu_enumeracao(opcoes)
        try:
            if opcao == '0':
                break
            elif opcao == '1':
                admin_inserir()
            elif opcao == '2':
                admin_remover()
            elif opcao == '3':
                admin_alterar()
            elif opcao == '4':
                admin_imprimir()
        except KeyboardInterrupt:
            print("\nOperação interrompida!")
