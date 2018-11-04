#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Módulo de comunicação principal.

Esse módulo é onde dispara o menu principal:
a tela de login e a tela de cadastro.
"""


from teca import database
from teca import cadastro
from teca.usuario import tela_usuario
from teca.admin import tela_admin
from teca.bibliotecario import tela_bibliotecario
from teca import term
import getpass


def login_informacao(usuario):
    print('Login efetuado como: ')
    print('Nome: ', usuario.nome.upper())
    print('Permissão: ', usuario.permissao.upper())
    print('Tipo de usuário: ', usuario.tipo.upper())
    if usuario.tipo in ('aluno', 'professor'):
        extra = usuario.extra
        if extra:
            print('Curso: ', extra.nome_curso.upper())


def tela_login():
    print('== LOGIN ==')
    while True:
        nickname = input('> Usuário: ')
        senha = getpass.getpass(prompt='> Senha: ')
        usuario = database.login(nickname, senha)
        if usuario:
            login_informacao(usuario)
            if usuario.permissao == 'administrador':
                tela_admin()
            elif usuario.permissao == 'bibliotecario':
                tela_bibliotecario()
            elif usuario.permissao == 'usuario':
                tela_usuario(usuario.matricula)
            break
        else:
            print("Usuário ou senha inválidos! Tente novamente.")


def main():
    # ------------LOGIN INICIAL-----------------
    print("Seja bem-vindo a TECA! Pressione Ctrl-C para interromper a tela.")
    while True:
        opcoes = {
            '1': 'Login',
            '2': 'Cadastro'
        }
        try:
            op = term.menu_enumeracao(opcoes)
        except (KeyboardInterrupt, EOFError):
            print("\nSaindo? Adeus então.")
            break

        try:
            if op == '1':
                tela_login()
            elif op == '2':
                cadastro.tela_cadastro_usuario()
        except (KeyboardInterrupt, EOFError):
            print('\nOperação cancelada!')


if __name__ == '__main__':
    main()
