#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Módulo define funções responsáveis para checar sanidade de valores.

Cada função de check de sanidade deve receber uma string e retornar
uma instância das classes filhas de ErrorMessage: sendo Ok ou Error.
"""


from datetime import datetime
from teca import database


class ErrorMessage(object):

    def __init__(self, message, status):
        self.message = message
        self.status = status

    def __bool__(self):
        return self.status

    def __str__(self):
        return self.message


class Error(ErrorMessage):

    def __init__(self, message):
        super().__init__(message, False)


class Ok(ErrorMessage):

    def __init__(self, message):
        super().__init__(message, True)


def data(data_string, format='%Y-%m-%d'):
    try:
        datetime.strptime(data_string, format)
        return Ok("Data é válida")
    except Exception:
        return Error("Data é inválida")


def matricula(matricula):
    if not matricula.isdecimal():
        return Error("Matricula deve ser um inteiro positivo!")
    elif database.Usuario.select(matricula) is not None:
        return Error("Matrícula ocupada!")
    else:
        return Ok("Matrícula ok!")


def nao_vazia(entrada):
    if len(entrada) == 0:
        return Error("Entrada não pode ser vazia!")
    return Ok("Entrada ok!")


def nome(nome):
    if not nome.replace(' ', '').isalpha():
        return Error("Nome deve ter apenas letras!")
    elif len(nome) == 0:
        return Error("Nome não pode ser vazio!")
    else:
        return Ok("Nome ok!")


def endereco(endereco):
    if len(endereco) == 0:
        return Error("Endereço não pode ser vazio!")
    else:
        return Ok("Endereço ok!")


def senha(senha):
    if len(senha) == 0:
        return Error("Senha não pode ser vazia!")
    else:
        return Ok("Senha ok!")

def cpf(cpf):
    if len(cpf) != 11 and not cpf.isdecimal():
        return Error("cpf deve possuir 11 dígitos!")
    else:
        return Ok("cpf ok!")


def nickname(nickname):
    if len(database.Usuario.filter(nickname=nickname)) != 0:
        return Error("Nickname já existe!")
    elif len(nickname) == 0:
        return Error("Nickname não pode ser vazio!")
    else:
        return Ok("Nickname ok!")


def telefone(telefone):
    if not telefone.isdecimal():
        return Error("Telefone deve conter apenas dígitos!")
    elif len(telefone) not in range(8, 12):
        return Error("Telefone deve conter entre 8 a 12 dígitos!")
    else:
        return Ok("Telefone ok!")


def emprestimo(usuario, livro):
    emprestimos = usuario.emprestimos
    extra = usuario.extra
    if livro.disponiveis <= 0:
        return Error("Livro indisponível para empréstimo!")
    elif extra is None:
        return Error(f"Usuário possuí dados corrompidos na tabela {usuario.tipo!r}! Contacte o administrador.")
    elif len(emprestimos) >= extra.livros_max:
        return Error(f"Usuário já alcançou o limite de {extra.livros_max} empréstimos!")
    elif any(livro.isbn == e.isbn for e in emprestimos):
        return Error("Usuário já possuí um exemplar desse livro emprestado.")
    elif any(e.vencido for e in emprestimos):
        return Error("Usuário possui empréstimo(s) vencido(s)!")
    elif (livro.disponiveis - len(livro.reservas))<= 0:
        res = database.Reserva.filter(matricula = usuario.matricula, isbn = livro.isbn)
        if len(res) != 0 and res[0].data_contemplado is not None:
            return Ok("Emprestimo ok, usuario possui reserva contemplada.")
        else:
            return Error("Livro disponivel apenas para reservas contempladas!")
    return Ok("Empréstimo ok!")


def entrada(prompt, funcao_check):
    while True:
        entrada = input(prompt)
        status = funcao_check(entrada)
        if status:
            break
        else:
            print(status)
    return entrada


def ask(ask):
    if ask.lower() not in ('y', 'n'):
        return Error("Entrada inválida")
    else:
        return Ok("Entrada ok!")
