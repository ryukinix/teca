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

               
                while True:
                    matricula      = input('> Digite sua matricula\n>>>: ') 
                    if database.Usuario.select(matricula) is None:
                        break
                    else:
                        print("Matrícula ocupada!")

                nome           = input('>Qual o seu nome completo?\n>>>: ')
                endereco       = input('>Onde você mora?\n>>>: ')
    
                tipos = {
                    '1':'aluno',
                    '2':'professor',
                    '3':'funcionario'
                }


                print('> Você é aluno, professor ou outro funcionário?')
                for numero,tipo in tipos.items():
                    print(numero,tipo)
                while True:
                    tipo_usuario = input('\n>>>: ')
                    if tipo_usuario in tipos:
                        tipo = tipos[tipo_usuario]
                        break
                    else:
                        print('Opção inválida')
                                        
                while True:
                    nickname = input('>Digite um nickname para acesso a sua conta: ')
                    if len(database.Usuario.filter(nickname=nickname)) == 0 :
                        break
                    else:
                        print("Nickname já existe!") 

                senha_cadastro = getpass.getpass(prompt='>Digite uma senha: ')


                #-----Tela de cadastramento do usuário ALUNO    
                if(tipo_usuario == '1'):   

                            #----Entradas do ALUNO                  
                            cod_curso            = input('> Digite o código de seu curso\n>>>: ')
                            data_de_ingresso     = input('> Em que ano,mês e dia você entrou na UFC?(YYYY-MM-DD)\n>>>: ')
                            data_de_conclusao    = input('> Em que ano,mês e dia você vai concluir seu curso?(YYYY-MM-DD)\n>>>: ')
                            
                            #----Impressão dos dados ALUNO digitados
                            print('\n')
                            print('Código do curso: '+cod_curso+'\n')
                            print('Data de ingresso no curso: '+data_de_ingresso+'\n')
                            print('Data de conclusão do curso: '+data_de_conclusao+'\n')

                #-----Tela de cadastramento do usuário PROFESSOR
                if(tipo_usuario == '2'):     
                                  
                            #----Entradas do PROFESSOR
                            data_de_contratacao  = input('> Em que ano, mês e dia você foi contratado pela UFC?(YYYY-MM-DD)\n>>>: ')
                            regime_de_trabalho   = input('> O seu regime de trabalho é de quantas horas?(DE|20H|40H)\n>>>: ')
                            cod_curso            = input('> Qual o código do curso que você leciona?\n>>>: ')
                            
                            #----Impressão dos dados PROFESSOR digitados
                            print('\n')
                            print('Data de contração: '+data_de_contratacao+'\n')
                            print('Regime de trabalho: '+regime_de_trabalho+'\n')
                            print('Código do curso: '+cod_curso+'\n')


                #----Tela de cadastramento dos TELEFONES                
                telefones = []   
                while True:
                    telefone = input('> Digite um numero de telefone: ')
                    telefones.append(telefone)
                    ask_2    = input('> Tem mais algum telefone?(Y/N) ')
                    if (ask_2 == 'N'):
                        break

                confirmacao = input('Está certo dos dados o que você colocou?(Y/N):')

                if(confirmacao=='Y'):

                    database.Usuario(matricula, nickname, database.senha_hash(senha_cadastro), nome, endereco, tipo_usuario,'usuario').insert()
                    for telefone in telefones:
                        database.Telefones(matricula,telefone).insert()

                    if(tipo_usuario=='professor'):
                        #-----Inserção do banco de dados da tabela PROFESSOR
                        database.Professor(matricula, data_de_contratacao, regime_de_trabalho, cod_curso).insert()
                      

                    elif(tipo_usuario=='aluno'):
                        #-----Inserção do banco de dados da tabela PROFESSOR
                        database.Aluno(matricula, data_de_conclusao, data_de_ingresso, cod_curso).insert()
                   

                    elif(tipo_usuario=='funcionario'):
                        #-----Inserção do banco de dados da tabela PROFESSOR
                        database.Funcionario(matricula).insert()
                
                #----Finalização do cadastramento 
                print('USUÁRIO CADASTRADO!!')

if __name__ == '__main__':
    main()
