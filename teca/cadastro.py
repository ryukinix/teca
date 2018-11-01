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

    # -----FIM DO CADASTRAMENTO INICAL DO USUARIO----- #
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
    while True:
        print('> Em que ano, mês e dia você entrou na UFC? (YYYY-MM-DD)')
        data_de_ingresso = input('>>> ')
        if check.data(data_de_ingresso):
            break
        else:
            print('Data inválida!')
    while True:
        print('> Em que data você vai concluir seu curso? (YYYY-MM-DD)')
        data_de_conclusao = input('>>> ')
        if check.data(data_de_conclusao):
            break
        else:
            print("Data inválida")

    # -----CHECK----- #
    print('\n')
    print('Código do curso: ', cod_curso)
    print('Data de ingresso no curso: ', data_de_ingresso)
    print('Data de conclusão do curso: ', data_de_conclusao)
    # -----FIM DO CADASTRO DO ALUNO----- #

    aluno = database.Aluno(matricula, data_de_conclusao,
                           data_de_ingresso, cod_curso)
    return aluno


def entrada_professor(matricula):
    cod_curso = entrada_curso()

    while True:
        print('> Em que data você foi contratado pela UFC? (YYYY-MM-DD)')
        data_de_contratacao = input('>>> ')
        if check.data(data_de_contratacao):
            break
        else:
            print("Data inválida")

    tipos_regime = {
        '1': 'DE',
        '2': '20H',
        '3': '40H'
    }
    print('> O seu regime de trabalho é de quantas horas?')
    op = menu_enumeracao(tipos_regime)
    regime_de_trabalho = tipos_regime[op]

    # -----CHECK----- #
    print('\n')
    print('Data de contração: '+data_de_contratacao+'\n')
    print('Regime de trabalho: '+regime_de_trabalho+'\n')
    print('Código do curso: '+cod_curso+'\n')

    prof = database.Professor(matricula, data_de_contratacao,
                              regime_de_trabalho, cod_curso)
    return prof


def entrada_telefones(matricula):
    telefones = []
    while True:
        telefone = input('> Digite um numero de telefone: ')

        if not telefone.isdecimal():
            print('Entrada inválida! Telefone precisa ser um número.')
            continue
        elif len(str(telefone)) not in range(8, 12):
            print('Telefone deve conter de 8 a 11 digitos.')
            continue

        telefones.append(database.Telefones(matricula, telefone))

        while True:
            ask = input('> Tem mais algum telefone? (Y/N) ')
            if ask.lower() not in ('y', 'n'):
                print('Entrada inválida')
            else:
                break

        if (ask.lower() == 'n'):
            break

    return telefones


def tela_cadastro_usuario():
    print('== CADASTRO DE USUÁRIO ==')

    # Entradas para todos os tipos de usuário
    usuario = entrada_usuario_comum()
    telefones = entrada_telefones(usuario.matricula)
    # Entradas especiais por tipo de usuário
    if usuario.tipo == 'aluno':
        aluno = entrada_aluno(usuario.matricula)
    elif usuario.tipo == 'professor':
        professor = entrada_professor(usuario.matricula)

    confirmacao = input('\nEstá certo os dados que você inseriu? (Y/N):')
    # -----INICIO INSERÇÃO NO BANCO DE DADOS----- #
    if confirmacao.lower() == 'y':
        usuario.insert()
        for telefone in telefones:
            telefone.insert()
        if usuario.tipo == 'aluno':
            aluno.insert()
        elif usuario.tipo == 'professor':
            professor.insert()
        elif usuario.tipo == 'funcionario':
            database.Funcionario(usuario.matricula).insert()
        print('USUÁRIO CADASTRADO!')
    # -----FIM INSERÇÃO NO BANCO DE DADOS----- #
