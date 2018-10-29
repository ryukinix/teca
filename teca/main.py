#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import database
import hashlib


def main():
    print("Seja bem vindo a TECA!")
    while True:
        nickname = input('> Usuário: ')
        senha = input('> Senha: ')
        usuario = database.login(nickname, senha)
        if usuario:
            print('Login efetuado como: ')
            print('Nome: ', usuario.nome.upper())
            print('Permissão: ', usuario.permissao.upper())
            print('Tipo de usuário: ', usuario.tipo.upper())
            break
        else:
            print("Usuário ou senha inválidos! Tente novamente.")


if __name__ == '__main__':
    main()
