#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import database
import hashlib

def main():
    dd = database.Database.connect()

    print("Seja bem vindo a TECA!")
    while True:
        ask = input(' Já é cadastro? Y/N ')

        if (ask=='Y'):

            nickname = input('> Usuário: ')
            senha = input('> Senha: ')
            login = database.login(nickname, senha)

            if login:

                print('Login efetuado como: ')
                print('Nome: ', login.nome.upper())
                print('Permissão: ', login.permissao.upper())
                print('Tipo de usuário: ', login.tipo.upper())
                break
            else:
                print("Usuário ou senha inválidos! Tente novamente.")       
                 
        if (ask=='N'):            

                print('Então vamos lhe cadastrar!!')

                matricula      = input('Digite sua matricula: ') 
                tipo_usuario   = input('> Você é aluno, professor ou outro funcionário? ')
                nome           = input('Qual o seu nome completo? ')
                endereco       = input('Onde você mora? ')
                nickname       = input('Digite um nickname para acesso de sua conta: ')
                senha_cadastro = input('Digite uma senha: ')

                database.Usuario(matricula, nickname, database.senha_hash(senha_cadastro), nome, endereco, tipo_usuario,'usuario').insert()

                while True:
                    telefone = input('> Digite um numero de telefone: ')
                    database.Telefones(matricula,telefone).insert()
                    ask_2 = input('> Tem mais algum telefone? Y/N ')
                    if (ask_2 == 'N'):
                            break

                print('USUÁRIO CADASTRADO!!')

if __name__ == '__main__':
    main()
