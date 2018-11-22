# coding: utf-8
from teca.bibliotecario import selecionar_livro
from teca import database
from teca import term
from datetime import datetime


def imprimir_livro(livro):
    for attr, value in livro.items():
        if attr == 'cod_categoria':
            attr = 'categoria'
            value = livro.categoria
        print(f"{attr}: {value}")
    print("emprestimos: ", len(livro.emprestimos))
    print("reservas: ", len(livro.reservas))


def consulta_livro():
    opcoes = {
        '1': 'Pesquisar por editora',
        '2': 'Pesquisar por categoria',
        '3': 'Pesquisar por titulo',
        '4': 'Pesquisar por autor',
        '5': 'Pesquisar por ano de publicação'
    }
    print("Opções: ")
    opcao = term.menu_enumeracao(opcoes)
    if opcao == '1':
        ed = input('Digite a editora: ')
        livros = database.Livro.search(ed, ['editora'])
        for livro in livros:
            print("======================")
            imprimir_livro(livro)
        print("======================")

    elif opcao == '2':
        cat = database.Categoria.select_all()
        for c in cat:
            print("======================")
            for nome_atributo in c._columns:
                valor_atributo = getattr(c, nome_atributo)
                print(f"{nome_atributo}: {valor_atributo}")
        print("======================")
        a = input('Digite o codigo da categoria escolhida: ')
        categoria = database.Categoria.select(a)
        tuplas = categoria.livros
        for tupla in tuplas:
            print("======================")
            imprimir_livro(tupla)
        print("======================")

    elif opcao == '3':
        a = input('Digite o titulo do livro: ')
        tuplas = database.Livro.search(a, ['titulo'])
        for tupla in tuplas:
            print("======================")
            imprimir_livro(tupla)
        print("======================")

    elif opcao == '4':
        aut = input('Digite o nome do autor: ')
        autores = database.Autor.search(aut, ['nome'])
        for autor in autores:
            livros = autor.livros
            for livro in livros:
                print("======================")
                imprimir_livro(livro)
            print("======================")

    elif opcao == '5':
        a = input('Digite o ano da publicação: ')
        livros = database.Livro.filter(ano=a)
        for livro in livros:
            print("======================")
            imprimir_livro(livro)
        print("======================")


def ver_emprestimo(usuario):
    emprestimos = usuario.emprestimos
    print("== EMPRESTIMOS")
    for e in emprestimos:
        print("==============")
        l = database.Livro.select(e.isbn)
        data_de_emprestimo = e.data_de_emprestimo.strftime("%d/%m/%Y")
        data_de_devolucao = e.data_de_devolucao.strftime("%d/%m/%Y")
        print("Título: ", l.titulo)
        print("ISBN: ", l.isbn)
        print("Data de empréstimo: ", data_de_emprestimo)
        print("Data de devolução: ", data_de_devolucao)
    print("==============")


def ver_reserva(usuario):
    reservas = usuario.reservas
    print("== RESERVAS")
    for e in reservas:
        print("==============")
        l = database.Livro.select(e.isbn)
        data_de_reserva = e.data_de_reserva.strftime("%d/%m/%Y")
        print("Título: ", l.titulo)
        print("ISBN: ", l.isbn)
        print("Data de reserva: ", data_de_reserva)
        print("Data Contemplado: ", e.data_contemplado)
    print("==============")


def realizar_reserva(usuario):
    livro = selecionar_livro()
    if (len(livro.emprestimos) + len(livro.emprestimos)) < livro.qt_copias:
        database.Reserva(usuario.matricula , livro.isbn, datetime.now(), datetime.now()).insert()
        print("Reserva realizada com sucesso!")
    else:
        database.Reserva(usuario.matricula , livro.isbn, datetime.now(), None).insert()
        print("Reserva realizada com sucesso!")


def excluir_cadastro(usuario):
    if len(usuario.emprestimos) == 0:
        usuario.delete()
        return True
    else:
        print('Usuario possui emprestimos pendentes!\n')
        return False


def tela_usuario(mat):
    print("== TELA DE USUÁRIO ==")
    while True:
        usuario = database.Usuario.select(mat)
        opcoes = {
            '1': 'Ver empréstimos',
            '2': 'Realizar reserva',
            '3': 'Excluir cadastro',
            '4': 'Consultar livros',
            '5': 'Ver reservas',
            '0': 'Sair'
        }

        opcao = term.menu_enumeracao(opcoes)
        try:
            if opcao == '1':
                ver_emprestimo(usuario)
            elif opcao == '2':
                realizar_reserva(usuario)
            elif opcao == '3':
                status = excluir_cadastro(usuario)
                if status:
                    break
            elif opcao == '4':
                consulta_livro()
            elif opcao == '5':
                ver_reserva(usuario)
            elif opcao == '0':
                break
            else:
                print("Opção inválida!")
        except KeyboardInterrupt:
            print("\nOperação interrompida!")
