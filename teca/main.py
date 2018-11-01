#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import database
from teca import cadastro
import getpass


def tela_login():
    print('== LOGIN ==')
    while True:
        nickname = input('> Usuário: ')
        senha = getpass.getpass(prompt='> Senha: ')
        usuario = database.login(nickname, senha)
        if usuario:
            print('Login efetuado como: ')
            print('Nome: ', usuario.nome.upper())
            print('Permissão: ', usuario.permissao.upper())
            print('Tipo de usuário: ', usuario.tipo.upper())
            if usuario.tipo in ('aluno', 'professor'):
                print('Curso: ', usuario.extra.nome_curso.upper())
            break
        else:
            print("Usuário ou senha inválidos! Tente novamente.")


def main():
    # ------------LOGIN INICIAL-----------------
    print("Seja bem-vindo a TECA! Pressione Ctrl-C para interromper a tela.")
    while True:
        try:
            ask = input('> Já é cadastrado? (Y/N): ')
        except KeyboardInterrupt:
            print("\nSaindo? Adeus então.")
            break

        if (ask.lower() == 'y'):
            try:
                tela_login()
            except KeyboardInterrupt:
                print('\nLogin interrompido!')
        elif (ask.lower() == 'n'):
            try:
                cadastro.tela_cadastro_usuario()
            except KeyboardInterrupt:
                print('\nCadastro interrompido!')


if __name__ == '__main__':
    main()
