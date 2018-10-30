#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import database
import hashlib
import getpass

def main():
    db = database.Database.connect()

    print("Seja bem vindo a TECA!")


#------Inicio da tela de teca:

    while True:
        ask = input(' Já é cadastrado? Y/N ')

        if (ask=='Y'):
            nickname = input('> Usuário: ')
            senha = getpass.getpass(prompt='>Senha: ')
            login = database.login(nickname, senha)
            if login:
                print('Login efetuado como: ')
                print('Nome: ', login.nome.upper())
                print('Permissão: ', login.permissao.upper())
                print('Tipo de usuário: ', login.tipo.upper())
                break
            else:
                print("Usuário ou senha inválidos! Tente novamente.")   
                    
#------Tela de cadastramento            
     
        if (ask=='N'):        
         
                #-----Entradas do USUÁRIO
                print('Então vamos lhe cadastrar!!')
                matricula      = input('> Digite sua matricula\n>>>: ') 
                nome           = input('>Qual o seu nome completo?\n>>>: ')
                endereco       = input('>Onde você mora?\n>>>: ')
                tipo_usuario   = input('> Você é aluno, professor ou outro funcionário?\n>>>: ')  
                nickname       = input('>Digite um nickname para acesso a sua conta: ')
                senha_cadastro = getpass.getpass(prompt='>Digite uma senha: ')

                #-----Inserção do banco de dados da tabela USUARIO
                database.Usuario(matricula, nickname, database.senha_hash(senha_cadastro), nome, endereco, tipo_usuario,'usuario').insert()        

                #-----Tela de cadastramento do usuário ALUNO    
                if(tipo_usuario == 'aluno'):   

                        while True:   
                            #----Entradas do ALUNO                  
                            cod_curso            = input('> Digite o código de seu curso\n>>>: ')
                            data_de_ingresso     = input('> Em que ano,mês e dia você entrou na UFC?(YYYY-MM-DD)\n>>>: ')
                            data_de_conclusao    = input('> Em que ano,mês e dia você vai concluir seu curso?(YYYY-MM-DD)\n>>>: ')
                            
                            #----Impressão dos dados ALUNO digitados
                            print('\n')
                            print('Matricula: '+matricula+'\n')
                            print('Código do curso: '+cod_curso+'\n')
                            print('Data de ingresso no curso: '+data_de_ingresso+'\n')
                            print('Data de conclusão do curso: '+data_de_conclusao+'\n')
                            confirmacao = input('Está certo os dados o que você colocou?(Y/N): ')

                            if(confirmacao=='Y'):
                                #-----Inserção do banco de dados da tabela ALUNO
                                database.Aluno(matricula, data_de_conclusao, data_de_ingresso, cod_curso).insert()
                                break

                #-----Tela de cadastramento do usuário PROFESSOR
                if(tipo_usuario == 'professor'):     
                                   
                        while True:   
                            #----Entradas do PROFESSOR
                            matricula_siape      = input('> Digite sua matricula Siape\n>>>: ')
                            data_de_contratacao  = input('> Em que ano, mês e dia você foi contratado pela UFC?(YYYY-MM-DD)\n>>>: ')
                            regime_de_trabalho   = input('> O seu regime de trabalho é de quantas horas?(DE|20H|40H)\n>>>: ')
                            cod_curso            = input('> Qual o código do curso que você leciona?\n>>>: ')
                            
                            #----Impressão dos dados PROFESSOR digitados
                            print('\n')
                            print('Matricula Siape: '+matricula_siape+'\n')
                            print('Data de contração: '+data_de_contratacao+'\n')
                            print('Regime de trabalho: '+regime_de_trabalho+'\n')
                            print('Código do curso: '+cod_curso+'\n')
                            confirmacao = input('Está certo dos dados o que você colocou?(Y/N):')

                            if(confirmacao=='Y'):
                                #-----Inserção do banco de dados da tabela PROFESSOR
                                database.Professor(matricula_siape, data_de_contratacao, regime_de_trabalho, cod_curso).insert()
                                break

                #-----Tela de cadastramento do usuário FUNCIONARIO
                if(tipo_usuario == 'funcionario'):

                        while True:
                            #----Impressão dos dados FUNCIONARIO digitados
                            matricula_funcionario = input('> Digite sua matricula\n>>>: ')
                            print('\n')
                            print('Matricula de funcionario: '+matricula_funcionario+'\n')
                            confirmacao = input('Está certo dos dados o que você colocou?(Y/N): ')

                            if(confirmacao == 'Y'):
                                #-----Inserção do banco de dados da tabela FUNCIONARIO
                                database.Funcionario(matricula_funcionario).insert()
                                break

                #----Tela de cadastramento dos TELEFONES                   
                while True:
                    telefone = input('> Digite um numero de telefone: ')

                    #-----Inserção do banco de dados da tabela TELEFONES
                    database.Telefones(matricula,telefone).insert()
                    ask_2 = input('> Tem mais algum telefone?(Y/N) ')
                    if (ask_2 == 'N'):
                            break
            
                #----Finalização do cadastramento 
                print('USUÁRIO CADASTRADO!!')

if __name__ == '__main__':
    main()
