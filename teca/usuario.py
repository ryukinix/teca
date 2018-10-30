from teca import database
from datetime import datetime

def consulta_livro():
    pass

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
            break