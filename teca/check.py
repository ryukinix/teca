#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from teca import database


class ErrorMessage(object):

    def __init__(self, mensagem, status):
        self.mensagem = mensagem
        self.status = status

    def __bool__(self):
        return self.status

    def __str__(self):
        return self.mensagem


class Error(ErrorMessage):

    def __init__(self, mensagem):
        super().__init__(mensagem, False)


class Ok(ErrorMessage):

    def __init__(self, mensagem):
        super().__init__(mensagem, True)


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


def endereco(endereco):#tratrar !! so string
    if len(endereco) == 0:
        return Error("Endereço não pode ser vazio!")
    else:
        return Ok("Endereço ok!")


def senha(senha):#tratrar !! so string  
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


def telefone(telefone):
    if not telefone.isdecimal():
        return Error("Telefone deve conter apenas dígitos!")
    elif len(telefone) not in range(8, 12):
        return Error("Telefone deve conter entre 8 a 12 dígitos!")
    else:
        return Ok("Telefone ok!")


def entrada(prompt, funcao_check):
    while True:
        entrada = input(prompt)
        status = funcao_check(entrada)
        if status:
            break
        else:
            print(status)
    return entrada


def data_de_ingresso(data_de_ingresso):
    if data(data_de_ingresso):
        return Ok("Data ok!")
    else:
        return Error("Data inválida!")

def data_de_conclusao(data_de_conclusao):
    if data(data_de_conclusao):
        return Ok("Data ok!")
    else:
        return Error("Data inválida")

def data_de_contracao():
    if data(data_de_conclusao):
        return Ok("Data ok!")
    else:
        return Error("Data inválida!")

def ask(ask):
    if ask.lower() not in ('y','n'):
        return Error("Entrada inválida")
    else:
        return Ok("Entrada ok!")

def telefones(telefones):
    if not telefones.isdecimal():
        return Error("Entrada inválida! Telefone precisa ser um número.")    
    elif len(str(telefones)) not in range(8, 12):
        return Error("Telefone deve conter de 8 a 11 digitos.")
    else:
        return Ok("Telefone ok!")