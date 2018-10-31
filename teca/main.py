#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import database
from datetime import datetime
import getpass


def data_valida(data_string, format='%Y-%m-%d'):
    try:
        datetime.strptime(data_string, format)
        return True
    except Exception:
        return False


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


def entrada_usuario_comum():
    # --- INICIO DA ENTRADA DA MATRICULA --- #
    while True:
        matricula = input('> Digite sua matricula\n>>> ')
        if not matricula.isdecimal():
            print("Matricula deve ser um inteiro!")
        elif database.Usuario.select(matricula) is None:
            break
        else:
            print("Matrícula ocupada!")
    # --- FIM DA ENTRADA DA MATRICULA --- #

    while True:
        nome = input('> Qual o seu nome completo?\n>>> ')
        if len(nome) != 0:
            break
        else:
            print('Você tem um nome! Digite.')

    while True:
        endereco = input('> Onde você mora?\n>>> ')
        if len(endereco) != 0:
            break
        else:
            print('Você mora em algum lugar!')

    # ---INICIO DA ENTRADA DO TIPO DE USUARIO--- #
    tipos = {
        '1': 'aluno',
        '2': 'professor',
        '3': 'funcionario'
    }
    print('> Você é aluno, professor ou outro funcionário?')
    escolha = menu_enumeracao(tipos)
    tipo = tipos[escolha]

    # --- FIM DA ENTRADA DO TIPO DE USUARIO --- #

    # --- INICIO DA ENTRADA DO NICKNAME --- #
    while True:
        nickname = input('> Digite um nickname para acesso a sua conta: ')
        if len(database.Usuario.filter(nickname=nickname)) == 0:
            break
        elif len(nickname) == 0:
            print("Nickname não pode ser vazio!")
        else:
            print("Nickname já existe!")

    while True:
        senha_cadastro = getpass.getpass(prompt='> Digite uma senha: ')
        if len(senha_cadastro) != 0:
            break
        else:
            print('Senha inválida!')

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
        if data_valida(data_de_ingresso):
            break
        else:
            print('Data inválida!')
    while True:
        print('> Em que data você vai concluir seu curso? (YYYY-MM-DD)')
        data_de_conclusao = input('>>> ')
        if data_valida(data_de_conclusao):
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
        if data_valida(data_de_contratacao):
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
                tela_cadastro_usuario()
            except KeyboardInterrupt:
                print('\nCadastro interrompido!')


if __name__ == '__main__':
    main()
