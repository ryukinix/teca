#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import check
from teca import database
import getpass


def menu_enumeracao(opcoes):
    """Constroi um menu de enumeração como pergunta."""
    for escolha, item in opcoes.items():
        print(f'{escolha}. {item.upper()}')
    while True:
        op = input('>>> ')
        if op in opcoes:
            break
        else:
            print('Opção inválida')

    return op


def entrada_usuario_comum():
    matricula = check.entrada('> Digite sua matricula\n>>> ', check.matricula)
    nome = check.entrada('> Qual o seu nome completo?\n>>> ', check.nome)
    endereco = check.entrada('> Onde você mora?\n>>> ', check.endereco)
    tipos = {
        '1': 'aluno',
        '2': 'professor',
        '3': 'funcionario'
    }
    print('> Você é aluno, professor ou outro funcionário?')
    escolha = menu_enumeracao(tipos)
    tipo = tipos[escolha]
    nickname = check.entrada('> Digite um nickname para acesso a sua conta: ',
                             check.nickname)

    while True:
        senha_cadastro = getpass.getpass(prompt='> Digite uma senha: ')
        status = check.senha(senha_cadastro)
        if status:
            break
        else:
            print(status)

    permissao = 'usuario'
    senha_hash = database.senha_hash(senha_cadastro)
    usuario = database.Usuario(matricula, nickname,
                               senha_hash, nome,
                               endereco, tipo, permissao)
    return usuario


def entrada_curso():
    cursos = {str(c.cod_curso): c.nome_curso
              for c in database.Curso.select_all()}
    print('> Digite o código de seu curso')
    cod_curso = menu_enumeracao(cursos)
    return cod_curso


def entrada_aluno(matricula):
    cod_curso = entrada_curso()
    print('> Em que ano, mês e dia você entrou na UFC? (YYYY-MM-DD)')
    data_de_ingresso = check.entrada('>>> ', check.data)
    print('> Em que data você vai concluir seu curso? (YYYY-MM-DD)')
    data_de_conclusao = check.entrada('>>> ', check.data)

    aluno = database.Aluno(matricula, data_de_conclusao,
                           data_de_ingresso, cod_curso)
    return aluno


def entrada_professor(matricula):
    cod_curso = entrada_curso()

    print('> Em que data você foi contratado pela UFC? (YYYY-MM-DD)')
    data_de_contratacao = check.entrada('>>> ', check.data)
    tipos_regime = {
        '1': 'DE',
        '2': '20H',
        '3': '40H'
    }
    print('> O seu regime de trabalho é de quantas horas?')
    op = menu_enumeracao(tipos_regime)
    regime_de_trabalho = tipos_regime[op]

    prof = database.Professor(matricula, data_de_contratacao,
                              regime_de_trabalho, cod_curso)
    return prof


def entrada_telefones(matricula):
    telefones = []

    while True:
        telefone = check.entrada('> Digite um numero de telefone: ',
                                 check.telefone)
        telefones.append(database.Telefones(matricula, telefone))
        ask = input('> Tem mais algum telefone? (Y/N) ')
        if ask.lower() != 'y':
            break

    return telefones


def tela_cadastro_usuario():
    print('== CADASTRO DE USUÁRIO ==')

    usuario = entrada_usuario_comum()
    telefones = entrada_telefones(usuario.matricula)
    if usuario.tipo == 'aluno':
        extra = entrada_aluno(usuario.matricula)
    elif usuario.tipo == 'professor':
        extra = entrada_professor(usuario.matricula)
    else:
        extra = database.Funcionario(usuario.matricula)

    print("== DADOS INSERIDOS: ")
    for attr, value in usuario.items():
        if attr == 'senha_hash':
            value = '*' * 8
            attr = 'senha'
        print(f"{attr}: {value}")

    for attr, value in extra.items():
        if attr not in extra._primary_key:
            print(f"{attr}: {value}")


    ask = check.entrada('\nEstá certo os dados que você inseriu? (Y/N):', check.ask)
    if ask == 'y':
        usuario.insert()
        extra.insert
        for telefone in telefones:
            telefone.insert()
        print('USUÁRIO CADASTRADO!')
    print('CADASTRO CANCELADO!')
