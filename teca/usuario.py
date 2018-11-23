# coding: utf-8
from teca.bibliotecario import selecionar_livro
from teca import database
from teca import term
from datetime import datetime
from tabulate import tabulate


def imprimir_livros(livros):
    rows = [list(l) + [l.disponiveis] for l in livros]
    headers = database.Livro._columns + ['disponíveis']
    print(tabulate(rows, headers, 'psql'))


def consultar_livros():
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
        imprimir_livros(livros)

    elif opcao == '2':
        cats = database.Categoria.select_all()
        print('Categorias: ')
        rows = list(map(list, cats))
        print(tabulate(rows, database.Categoria._columns, 'psql'))

        a = input('Digite o codigo da categoria escolhida: ')
        categoria = database.Categoria.select(a)
        livros = categoria.livros
        imprimir_livros(livros)

    elif opcao == '3':
        a = input('Digite o titulo do livro: ')
        livros = database.Livro.search(a, ['titulo'])
        imprimir_livros(livros)

    elif opcao == 4:
        aut = input('Digite o nome do autor: ')
        autores = database.Autor.search(aut, ['nome'])
        for autor in autores:
            livros = autor.livros
            imprimir_livros(livros)

    elif opcao == '5':
        a = input('Digite o ano da publicação: ')
        livros = database.Livro.filter(ano=a)
        imprimir_livros(livros)


def consultar_emprestimos(usuario):
    emprestimos = usuario.emprestimos
    print("== EMPRESTIMOS")
    for e in emprestimos:
        print("==============")
        livro = database.Livro.select(e.isbn)
        data_de_emprestimo = e.data_de_emprestimo.strftime("%d/%m/%Y")
        data_de_devolucao = e.data_de_devolucao.strftime("%d/%m/%Y")
        print("Título: ", livro.titulo)
        print("ISBN: ", livro.isbn)
        print("Data de empréstimo: ", data_de_emprestimo)
        print("Data de devolução: ", data_de_devolucao)
    print("==============")


def consultar_reservas(usuario):
    reservas = usuario.reservas
    print("== RESERVAS")
    for e in reservas:
        print("==============")
        livro = database.Livro.select(e.isbn)
        data_de_reserva = e.data_de_reserva.strftime("%d/%m/%Y")
        print("Título: ", livro.titulo)
        print("ISBN: ", livro.isbn)
        print("Data de reserva: ", data_de_reserva)
        print("Data Contemplado: ", e.data_contemplado)
    print("==============")


def realizar_reserva(usuario):
    livro = selecionar_livro()
    now = datetime.now()
    ok = None
    if (len(livro.emprestimos) + len(livro.emprestimos)) < livro.qt_copias:
        res = database.Reserva(usuario.matricula, livro.isbn, now, now)
        ok = res.insert()
    else:
        res = database.Reserva(usuario.matricula, livro.isbn, now, None)
        ok = res.insert()

    if ok:
        print("Reserva realizada com sucesso!")


def excluir_cadastro(usuario):
    if len(usuario.emprestimos) == 0:
        ok = usuario.delete()
        if ok:
            print("Usuário deletado! Adeus")
        return ok

    print("Usuário possui empréstimos pendentes!")
    return False


def tela_usuario(mat):
    print("== TELA DE USUÁRIO ==")
    while True:
        usuario = database.Usuario.select(mat)
        opcoes = {
            '1': 'Consultar livros',
            '2': 'Consultar empréstimos',
            '3': 'Consultar reservas',
            '4': 'Realizar reserva',
            '5': 'Excluir cadastro',
            '0': 'Sair'
        }

        opcao = term.menu_enumeracao(opcoes)
        try:
            if opcao == '1':
                consultar_livros()
            elif opcao == '2':
                consultar_emprestimos(usuario)
            elif opcao == '3':
                consultar_reservas(usuario)
            elif opcao == '4':
                realizar_reserva(usuario)
            elif opcao == '5':
                status = excluir_cadastro(usuario)
                if status:
                    break
            elif opcao == '0':
                break
            else:
                print("Opção inválida!")
        except KeyboardInterrupt:
            print("\nOperação interrompida!")
