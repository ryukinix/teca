#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mysql_driver


class Database(object):

    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password
        self.conn = mysql_driver.connect(user=user, password=password,
                                         host='localhost',
                                         database=database)

    def query(self, sql, params):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        for result in cursor:
            yield {k: v for k, v in zip(cursor.column_names, result)}
        cursor.close()

    def first_result(self, sql, params):
        result = list(self.query(sql, params))
        if result:
            return result[0]
        return None

    def usuario(self, matricula):
        sql = ("SELECT * FROM usuario WHERE matricula=%s")
        params = (matricula,)
        return self.first_result(sql, params)

    def login(self, nome_usuario, senha):
        sql = ("SELECT matricula, nickname, senha FROM usuario "
               "WHERE (nickname=%s OR matricula=%s) AND senha=%s")
        params = (nome_usuario, nome_usuario, senha)
        login = self.first_result(sql, params)
        if not login:
            return None
        matricula = login['matricula']
        usuario = self.usuario(matricula)
        return usuario

    def close(self):
        self.conn.close()


def main():
    db = Database('equipe385145', 'root', 'root')
    print("Seja bem vindo a TECA!")
    while True:
        nickname = input('> Usuário: ')
        senha = input('> Senha: ')
        login = db.login(nickname, senha)
        if login:
            print('Login efetuado como: ')
            print('Nome: ', login['nome'].upper())
            print('Permissão: ', login['permissao'].upper())
            print('Tipo de usuário: ', login['tipo'].upper())
            break
        else:
            print("Usuário ou senha inválidos! Tente novamente.")


if __name__ == '__main__':
    main()
