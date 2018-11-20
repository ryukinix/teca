#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Interface de aplicação com o SGBD MySQL

Provê um simples modelo ORM (Object Relational Model)
implementado em Python.

Ex.:

>>> from teca import database
>>> u = database.Usuario.select(394192)
>>> u.nome
'Manoel Vilela'
"""

import mysql.connector as mysql_driver
import hashlib
import abc
from datetime import datetime
from datetime import timedelta


class Database(object):

    """Classe gerenciadora de conexão e consultas SQL"""

    instance = None

    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password
        self.conn = mysql_driver.connect(user=user, password=password,
                                         host='localhost',
                                         database=database)

    @classmethod
    def connect(cls):
        if not cls.instance:
            cls.instance = Database('equipe385145', 'root', 'root')
        return cls.instance

    def query(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        for result in cursor:
            yield result
        cursor.close()

    def commit(self, sql, params=()):
        cursor = self.conn.cursor()
        status = None
        try:
            cursor.execute(sql, params)
            status = self.conn.commit()
        except Exception as e:
            err_name = e.__class__.__name__
            print(f"Warning: Database.commit: {err_name}: {e}")
            status = self.conn.rollback()
        finally:
            cursor.close()

        return status

    def unsafe_commit(self, sql, params=()):
        cursor = self.conn.cursor()
        status = cursor.execute(sql, params)
        self.conn.commit()
        cursor.close()
        return status

    def first_result(self, sql, params=()):
        result = list(self.query(sql, params))
        if result:
            return result[0]
        return None

    def close(self):
        self.conn.close()


class Tabela(metaclass=abc.ABCMeta):

    """Classe abstrata para ser base de herança
    nas implementações de cada Tabela especializada.

    Provê métodos básicos para seleção, inserção, remoção e
    atualização.
    """

    # Para serem redefinidas quando a herança for feita
    _table = None
    _columns = []
    _primary_key = []

    def __init__(self, *args):
        expects = len(self._columns)
        got = len(args)
        if expects != got:
            cls = self.__class__.__name__
            a = self._columns
            err = f'{cls} expects {expects} arguments, got {got}. Args: {a!r}'
            raise TypeError(err)
        for k, v in zip(self._columns, args):
            setattr(self, k, v)

    def __repr__(self):
        cls_name = self.__class__.__name__
        values_format = [f'{k}={v!r}' for k, v in self.items()]
        attributes = ', '.join(values_format)
        return f'{cls_name}({attributes})'

    def __str__(self):
        attrs = []
        for attr, value in self.items():
            attrs.append(f"{attr}: {value}")
        return '\n'.join(attrs)

    def __iter__(self):
        for k in self._columns:
            if k in vars(self):
                yield getattr(self, k)

    def items(self):
        return list(zip(self._columns, iter(self)))

    def insert(self, unsafe=False):
        conn = Database.connect()
        table = self._table
        columns, values = zip(*self.items())
        params = ', '.join(['%s' for _ in range(len(columns))])
        sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({params})"
        if unsafe:
            return conn.unsafe_commit(sql, tuple(values))
        else:
            return conn.commit(sql, tuple(values))

    @classmethod
    def select(cls, pk, unpack=True):
        not_scalar = any(isinstance(pk, t) for t in [list, tuple])
        keys = len(pk) if not_scalar else 1
        conn = Database.connect()
        table = cls._table
        where_columns = cls._columns[0:keys]
        columns = cls._columns
        where = " AND ".join(map("{}=%s".format, where_columns))
        sql = f"SELECT {','.join(columns)} FROM {table} WHERE {where}"
        params = pk if not_scalar else (pk,)
        result = list(conn.query(sql, params))
        instances = [cls(*tuple(r)) for r in result]
        if not result and unpack:
            return None
        elif unpack:
            return instances[0]
        return instances

    @classmethod
    def filter(cls, pk=None, **kwargs):
        if pk:
            return cls.select(pk, unpack=False)
        else:
            conn = Database.connect()
            columns = cls._columns
            where_columns, values = zip(*kwargs.items())
            where = " AND ".join(map("{}=%s".format, where_columns))
            sql = f"SELECT {','.join(columns)} FROM {cls._table} WHERE {where}"
            return [cls(*r) for r in conn.query(sql, values)]

    @classmethod
    def select_all(cls):
        conn = Database.connect()
        table = cls._table
        columns = cls._columns
        sql = f"SELECT {','.join(columns)} FROM {table}"
        result = conn.query(sql)
        if not result:
            return None
        return [cls(*row) for row in result]

    @classmethod
    def search(cls, string, attrs=()):
        """Sistema de busca genérico por atributos e substrings.
        Retorna uma lista de candidatos possíveis dada a string passada.
        attrs deve ser uma sequência de strings com o nome das colunas
        de determinada tabela a serem usadas na pesquisa.
        Ex.:
        >>> Usuario.search('manoel', ['nome'])
        [Usuario(matricula='394192', nome='Manoel Vilela', ...)]
        """
        # procura por chave
        row = cls.select(string)
        if row:
            return [row]

        # procure por atributo (igual)
        for attr in attrs:
            if attr not in cls._columns:
                continue
            query = {attr: string}
            rows = cls.filter(**query)
            if len(rows) == 1:
                return rows

        # procura por substrings para cada atributo passado
        rows = cls.select_all()
        candidates = []
        string = string.lower()
        for r in rows:
            for attr in attrs:
                attr_value = str(getattr(r, attr))
                if string in attr_value.lower():
                    candidates.append(r)
                    break

        return candidates

    def delete(self):
        conn = Database.connect()
        table = self._table
        primary_key = self._primary_key
        primary_key_value = tuple(getattr(self, k) for k in primary_key)
        where = " AND ".join(map("{}=%s".format, primary_key))
        sql = f"DELETE FROM {table} WHERE {where}"
        return conn.commit(sql, primary_key_value)

    def update(self):
        conn = Database.connect()
        table = self._table
        columns, values = zip(*self.items())
        primary_key = self._primary_key
        primary_key_value = tuple(getattr(self, k) for k in primary_key)
        set_stmt = ", ".join(map("{}=%s".format, columns))
        where = " AND ".join(map("{}=%s".format, primary_key))
        sql = f'UPDATE {table} SET {set_stmt} WHERE {where}'
        params = values + primary_key_value
        return conn.commit(sql, params)


class Usuario(Tabela):

    _table = 'usuario'
    _columns = ['matricula', 'nickname', 'senha_hash',
                'nome', 'endereco', 'tipo', 'permissao']
    _primary_key = ['matricula']

    def mudar_senha(self, nova_senha):
        self.senha_hash = senha_hash(nova_senha)

    def gerar_emprestimo(self, isbn):
        mat = self.matricula
        prazo = timedelta(days=self.extra.prazo_max)
        data_de_emprestimo = datetime.now()
        data_de_devolucao = data_de_emprestimo + prazo
        return Emprestimo(mat, isbn, data_de_emprestimo, data_de_devolucao)

    @property
    def extra(self):
        if self.tipo == 'aluno':
            return Aluno.select(self.matricula)
        elif self.tipo == 'professor':
            return Professor.select(self.matricula)
        elif self.tipo == 'funcionario':
            return Funcionario.select(self.matricula)

    @property
    def telefones(self):
        return Telefones.filter(self.matricula)

    @property
    def emprestimos(self):
        return Emprestimo.filter(self.matricula)

    @property
    def reservas(self):
        return Reserva.filter(self.matricula)


class Aluno(Tabela):
    _table = 'aluno'
    _columns = ['matricula', 'data_de_conclusao_prevista',
                'data_de_ingresso', 'cod_curso']
    _primary_key = ['matricula']
    livros_max = 3
    prazo_max = 15

    @property
    def usuario(self):
        return Usuario.select(self.matricula)

    @property
    def nome_curso(self):
        return Curso.select(self.cod_curso).nome_curso

    def insert(self):
        return super().insert(unsafe=True)


class Professor(Tabela):
    _table = 'professor'
    _columns = ['mat_siape', 'data_de_contratacao', 'regime_trabalho',
                'cod_curso']
    _primary_key = ['mat_siape']
    livros_max = 5
    prazo_max = 30

    @property
    def usuario(self):
        return Usuario.select(self.mat_siape)

    @property
    def nome_curso(self):
        return Curso.select(self.cod_curso).nome_curso


class Funcionario(Tabela):
    _table = 'funcionario'
    _columns = ['matricula']
    _primary_key = ['matricula']
    livros_max = 4
    prazo_max = 21

    @property
    def usuario(self):
        return Usuario.select(self.matricula)


class Livro(Tabela):
    _table = 'livro'
    _columns = ['isbn', 'titulo', 'ano', 'editora',
                'qt_copias', 'cod_categoria']
    _primary_key = ['isbn']

    @property
    def autores(self):
        autor_livro = AutorLivro.filter(livro_isbn=self.isbn)
        return list(map(lambda x: Autor.select(x.autor_cpf), autor_livro))

    @property
    def categoria(self):
        cat = Categoria.select(self.cod_categoria)
        return cat.descricao

    @property
    def emprestimos(self):
        return Emprestimo.filter(isbn=self.isbn)

    @property
    def reservas(self):
        return Reserva.filter(isbn=self.isbn)

    @property
    def disponiveis(self):
        return self.qt_copias - len(self.emprestimos)


class Reserva(Tabela):
    _table = 'reserva'
    _columns = ['matricula', 'isbn', 'data_de_reserva', 'data_contemplado']
    _primary_key = ['matricula']

    @property
    def livro(self):
        return Livro.select(self.isbn)

class Emprestimo(Tabela):
    _table = 'emprestimo'
    _columns = ['matricula', 'isbn', 'data_de_emprestimo', 'data_de_devolucao']
    _primary_key = ['matricula', 'isbn']

    @property
    def livro(self):
        return Livro.select(self.isbn)

    @property
    def vencido(self):
        return datetime.now().date() > self.data_de_devolucao


class Telefones(Tabela):
    _table = 'telefones'
    _columns = ['matricula', 'numero']
    _primary_key = ['matricula', 'numero']


class Autor(Tabela):
    _table = 'autor'
    _columns = ['cpf', 'nome', 'nacionalidade']
    _primary_key = ['cpf']

    @property
    def livros(self):
        autor_livro = AutorLivro.filter(self.cpf)
        return [Livro.select(k.livro_isbn) for k in autor_livro]


class AutorLivro(Tabela):
    _table = 'autor_livro'
    _columns = ['autor_cpf', 'livro_isbn']
    _primary_key = ['autor_cpf', 'livro_isbn']


class Curso(Tabela):
    _table = 'curso'
    _columns = ['cod_curso', 'nome_curso']
    _primary_key = ['cod_curso']

    @property
    def professores(self):
        return Professor.filter(cod_curso=self.cod_curso)

    @property
    def alunos(self):
        return Aluno.filter(cod_curso=self.cod_curso)


class Categoria(Tabela):
    _table = 'categoria'
    _columns = ['cod_categoria', 'descricao']
    _primary_key = ['cod_categoria']

    @property
    def livros(self):
        return Livro.filter(cod_categoria=self.cod_categoria)

ttabelas = [Usuario, Aluno, Funcionario, Professor, Curso, Telefones,
           Emprestimo, Reserva, Categoria, Livro, AutorLivro, Autor]
tabelas = [Usuario, Curso, Telefones,
           Emprestimo, Reserva, Categoria, Livro, AutorLivro, Autor]
sub_tabelas = [ Aluno, Funcionario, Professor]

def senha_hash(senha):
    return hashlib.sha256(senha.strip('\n').encode('utf-8')).hexdigest()


def login(nome_usuario, senha):
    conn = Database.connect()
    sql = ("SELECT matricula FROM usuario "
           "WHERE (nickname=%s OR matricula=%s) and senha_hash=%s")
    params = (nome_usuario, nome_usuario, senha_hash(senha))
    result = conn.first_result(sql, params)
    if result is None:
        return None
    matricula = result[0]
    usuario = Usuario.select(matricula)
    return usuario
