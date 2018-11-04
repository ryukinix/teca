#!/usr/bin/env python
# coding: utf-8

from teca import term
from teca import database
from teca import check


def sumario_emprestimo(e):
    return f'{e.isbn} / {e.livro.titulo} / {e.data_de_emprestimo}'


def sumario_reserva(r):
    return f'{r.isbn} / {r.livro.titulo} / {r.data_de_reserva}'


def sumario_livro(l):
    return f'{l.isbn} / {l.titulo} / {l.editora} / {l.ano} / {l.categoria}'


def sumario_usuario(u):
    return f'{u.matricula} / {u.nome}'


def imprimir_usuario(u):
    u.senha_hash = '*' * 8
    emps = u.emprestimos
    resv = u.reservas
    extra = u.extra
    print("== INFORMAÇÃO DE USUÁRIO")
    print(u)
    if extra:
        extra._column = [k for k in extra._columns
                         if k not in extra._primary_key]
        print(u.extra)
        if u.tipo in ('aluno', 'professor'):
            print("curso: ", extra.nome_curso)
    print("empréstimos: ", len(emps))
    print("reservas: ", len(resv))

    if emps:
        print("== EMPRÉSTIMOS")
        for idx, e in enumerate(emps):
            print(f"{idx + 1}. {sumario_emprestimo(e)}")
    if resv:
        print("== RESERVAS")
        for idx, r in enumerate(resv):
            print(f"{idx + 1}. {sumario_reserva(r)}")
    print("==================================")


def imprimir_livro(livro):
    print("== INFORMAÇÃO DO LIVRO")
    emprestimos = livro.emprestimos
    reservas = livro.reservas
    print(livro)
    print("categoria: ", livro.categoria)
    print("autores: ", ", ".join([a.nome for a in livro.autores]))
    print("empréstimos: ", len(emprestimos))
    print("reservados: ", len(reservas))
    print("disponíveis: ", livro.disponiveis)

    if len(emprestimos) > 0:
        print("== USUÁRIOS COM EMPRÉSTIMO", )
        for e in database.Emprestimo.filter(isbn=livro.isbn):
            u = database.Usuario.select(e.matricula)
            print("    ", sumario_usuario(u))
    if len(reservas) > 0:
        print("== USUÁRIOS COM RESERVA")
        for e in database.Reserva.filter(isbn=livro.isbn):
            u = database.Usuario.select(e.matricula)
            print("    ", sumario_usuario(u))


def selecionar_usuario():
    query = input("Pesquise por nome ou matrícula: ")
    usuarios = database.Usuario.search(query, ['nome'])
    if not usuarios:
        print("Nenhum usuário encontrado!")
        return selecionar_usuario()
    usuarios_map = {str(idx+1): u for idx, u in enumerate(usuarios)}
    usuarios_enum = {k: sumario_usuario(u)
                     for k, u in usuarios_map.items()}
    print("== USUÁRIOS")
    print("   matrícula / nome")
    op = term.menu_enumeracao(usuarios_enum)
    return usuarios_map[op]


def selecionar_livro():
    query = input("Pesquise por isbn, título, editora, categoria ou ano: ")
    livros = database.Livro.search(query, ['titulo', 'editora',
                                           'ano', 'categoria'])
    if not livros:
        print("Nenhum livro encontrado!")
        return selecionar_livro()
    livros_map = {str(idx+1): u for idx, u in enumerate(livros)}
    livros_enum = {k: sumario_livro(l)
                   for k, l in livros_map.items()}
    print("== LIVROS")
    print("   isbn / titulo / editora / ano / categoria")
    op = term.menu_enumeracao(livros_enum)
    return livros_map[op]


def consultar_usuarios():
    u = selecionar_usuario()
    if u:
        imprimir_usuario(u)
    else:
        print("Nenhum usuário encontrado!")


def consultar_livros():
    livro = selecionar_livro()
    imprimir_livro(livro)


# TODO: Implementar sistema de filtro
def consultar_reservas():
    term.imprimir_tabela(database.Reserva)


# TODO: Implementar sistema de filtro
def consultar_emprestimos():
    term.imprimir_tabela(database.Emprestimo)


def realizar_emprestimo():
    print("Escolha um usuário!")
    usuario = selecionar_usuario()
    livro = selecionar_livro()
    ok = check.emprestimo(usuario, livro)
    if not ok:
        print(ok)
        return None

    emprestimo = usuario.gerar_emprestimo(livro.isbn)
    check_reserva = [r for r in usuario.reservas
                     if livro.isbn == r.isbn]
    if check_reserva:
        print("Usuário possui reserva para esse livro!")
        reserva = check_reserva[0]
        reserva.delete()
        print("RESERVA CONSUMIDA!")

    emprestimo.insert()
    print("EMPRÉSTIMO REALIZADO!")


def dar_baixa_emprestimo():
    print("Escolha um usuário!")
    u = selecionar_usuario()
    emps = u.emprestimos
    if not emps:
        print("Usuário não possuí empréstimos")
        return None
    print("== EMPRÉSTIMOS: ")
    print("   isbn / título / data de empréstimo")
    emps_map = {str(idx+1): e for idx, e in enumerate(emps)}
    emps_enum = {k: sumario_emprestimo(v)
                 for k, v in emps_map.items()}
    op = term.menu_enumeracao(emps_enum)
    e = emps_map[op]
    e.delete()
    print("DEVOLUÇÃO DO EMPRÉSTIMO REALIZADA!")


def tela_bibliotecario():
    print("== BIBLIOTECÁRIO ==")
    while True:
        opcoes = {
            '1': 'Consultar usuários',
            '2': 'Consultar livros',
            '3': 'Consultar reservas',
            '4': 'Consultar empréstimos',
            '5': 'Realizar empréstimo',
            '6': 'Dar baixa empréstimo',
        }

        try:
            op = term.menu_enumeracao(opcoes)
        except KeyboardInterrupt:
            print()  # fix next print on terminal
            break

        try:
            if op == '1':
                consultar_usuarios()
            elif op == '2':
                consultar_livros()
            elif op == '3':
                consultar_reservas()
            elif op == '4':
                consultar_emprestimos()
            elif op == '5':
                realizar_emprestimo()
            elif op == '6':
                dar_baixa_emprestimo()
            else:
                print('Não implementado!')

            input("Pressione enter para continuar...")
        except KeyboardInterrupt:
            print("\nOperação interrompida!")


if __name__ == '__main__':
    tela_bibliotecario()
