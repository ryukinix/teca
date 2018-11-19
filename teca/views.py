# coding: utf-8


"""Módulo para listagem das views (visões) no banco de dados.
"""


from teca import term
from teca import database
from tabulate import tabulate


def gerar_tabela(sql, params=()):
    """Recebe uma consulta SQL e gera uma string formatada como tabela"""
    db = database.Database.connect()
    rows = []
    cursor = db.conn.cursor()
    cursor.execute(sql, params)
    for result in cursor:
        rows.append(result)
    headers = [k[0] for k in cursor.description]
    cursor.close()
    return tabulate(rows, headers, 'psql')


def view_livro_ano():
    tabela = gerar_tabela('SELECT * FROM view_livro_ano')
    print(tabela)


def view_livro_categoria():
    tabela = gerar_tabela('SELECT * FROM view_livro_categoria')
    print(tabela)


def view_livro_editora():
    tabela = gerar_tabela('SELECT * FROM view_livro_editora')
    print(tabela)


# TODO: filtro por curso
def view_professor_curso():
    tabela = gerar_tabela('SELECT * FROM view_professor_curso')
    print(tabela)


# TODO: filtro por livro
def view_reserva_livro():
    tabela = gerar_tabela('SELECT * FROM view_reserva_livro')
    print(tabela)


def view_livro_autores():
    tabela = gerar_tabela('SELECT * FROM view_livro_autores')
    print(tabela)


def tela_views():
    print("== VIEWS ==")
    while True:
        opcoes = {
            '1': 'Listar livros por ano',
            '2': 'Listar livros por categoria',
            '3': 'Listar livros por editora',
            '4': 'Listar livros por autor',
            '5': 'Listar professores por curso',
            '6': 'Listar reservas por livro e usuário',
            '0': 'Sair'
        }

        try:
            op = term.menu_enumeracao(opcoes)
        except KeyboardInterrupt:
            print()  # fix next print on terminal
            break

        try:
            if op == '1':
                view_livro_ano()
            elif op == '2':
                view_livro_categoria()
            elif op == '3':
                view_livro_editora()
            elif op == '4':
                view_livro_autores()
            elif op == '5':
                view_professor_curso()
            elif op == '6':
                view_reserva_livro()
            elif op == '0':
                break
            else:
                print('Não implementado!')

            input("Pressione enter para continuar...")
        except KeyboardInterrupt:
            print("\nOperação interrompida!")
