# coding: utf-8
from teca.bibliotecario import selecionar_livro
from teca import database
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
    opcoes = [
        'Pesquisar por editora',
        'Pesquisar por categoria',
        'Pesquisar por titulo',
        'Pesquisar por autor',
        'Pesquisar por ano de publicação'
        ]
    print("Opções: ")
    for i, op in enumerate(opcoes):
        print("{}. {}".format(i+1, op))

    while True:
            opcao = int(input(">>> "))
            if opcao in range(1, len(opcoes) + 1):
                break
            else:
                print("Opção invalida!")
    if opcao == 1:
        ed = input('Digite a editora: ')
        livros = database.Livro.search(ed, ['editora'])
        for livro in livros:
            print("======================")   
            imprimir_livro(livro)
        print("======================")

    elif opcao == 2:
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

    elif opcao == 3:
        a = input('Digite o titulo do livro: ')
        tuplas = database.Livro.search(a, ['titulo'])
        for tupla in tuplas:
            print("======================")
            imprimir_livro(tupla)
        print("======================")
    elif opcao == 4:
        aut = input('Digite o nome do autor: ')
        autores = database.Autor.search(aut, ['nome'])
        for autor in autores:
            livros = autor.livros
            for livro in livros:
                print("======================")   
                imprimir_livro(livro)
            print("======================")

    elif opcao == 5:
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
    print("==============")

def realizar_reserva(usuario):
    livro = selecionar_livro()
    if len(livro.emprestimos) < livro.qt_copias:
        print("Livro disponivel para emprestimo!")
    else:
        database.Reserva(usuario.matricula , livro.isbn, datetime.now()).insert()
        print("Reserva realizada com sucesso!")

def excluir_cadastro(usuario):
    if len(usuario.emprestimos) == 0:
        usuario.delete()
        return True
    else:
        print('Usuario possui emprestimos pendentes!\n')
        return False

def tela_usuario(mat):
    while True:
        usuario = database.Usuario.select(mat)
        opcoes = [
            'Ver emprestimos',
            'Realizar reserva',
            'Excluir cadastro',
            'Consultar livros',
            'ver reservas',
            'Sair'
        ]
        print("Opções: ")
        for i, op in enumerate(opcoes):
            print("{}. {}".format(i+1, op))

        while True:
            opcao = int(input(">>> "))
            if opcao in range(1, len(opcoes) + 1):
                break

        if opcao == 1:
            ver_emprestimo(usuario)
        elif opcao == 2:
            realizar_reserva(usuario)
        elif opcao == 3:
            status = excluir_cadastro(usuario)
            if status:
                break
        elif opcao == 4:
            consulta_livro()
        elif opcao == 5:
            ver_reserva(usuario)