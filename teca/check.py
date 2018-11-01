#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from teca import database


class Error(object):

    def __init__(self, mensagem):
        self.mensagem = mensagem

    def __bool__(self):
        return False

    def __str__(self):
        return self.mensagem


class Ok(object):

    def __init__(self, mensagem):
        self.mensagem = mensagem

    def __bool__(self):
        return True

    def __str__(self):
        return self.mensagem


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


def nome(nome):
    if len(nome) == 0:
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


def nickname(nickname):
    if len(database.Usuario.filter(nickname=nickname)) != 0:
        return Error("Nickname já existe!")
    elif len(nickname) == 0:
        return Error("Nickname não pode ser vazio!")
    else:
        return Ok("Nickname ok!")


def entrada(prompt, funcao_check):
    while True:
        entrada = input(prompt)
        status = funcao_check(entrada)
        if status:
            break
        else:
            print(status)
    return entrada
