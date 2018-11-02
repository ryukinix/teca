from teca import database
from datetime import datetime

def consulta_livro():
    opcoes = [
        'Pesquisar por editora',
        'Pesquisar por categoria',
        'Pesquisar por titulo'
        ]
    print("Opções: ")
    for i, op in enumerate(opcoes):
        print("{}. {}".format(i+1, op))

    while True:
            opcao = int(input(">>> "))
            if opcao in range(1, len(opcoes) + 1):
                break
    if opcao == 1:
        ed = input('Digite a editora: ')
        tuplas = database.Livro.filter(editora = ed)
        
        for tupla in tuplas:
            print("======================")
            for nome_atributo in tupla._columns:
                if nome_atributo == 'cod_categoria':
                    print('Categoria: ', tupla.categoria)
                else:  
                    valor_atributo = getattr(tupla, nome_atributo)
                    print(f"{nome_atributo}: {valor_atributo}")
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
            for nome_atributo in tupla._columns:
                if nome_atributo == 'cod_categoria':
                    print('Categoria: ', tupla.categoria)
                else:  
                    valor_atributo = getattr(tupla, nome_atributo)
                    print(f"{nome_atributo}: {valor_atributo}")
        print("======================")

    elif opcao == 3:
        a = input('Digite o titulo do livro: ')
        tuplas = database.Livro.filter(titulo = a)
        for tupla in tuplas:
            print("======================")
            for nome_atributo in tupla._columns:
                if nome_atributo == 'cod_categoria':
                    print('Categoria: ', tupla.categoria)
                else:  
                    valor_atributo = getattr(tupla, nome_atributo)
                    print(f"{nome_atributo}: {valor_atributo}")
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
        

def realizar_reserva(usuario):
    pass
    

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
            'Colsultar livros',
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

