#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from teca import database
import hashlib
import getpass

def main():
    db = database.Database.connect()

 #-------------------------------------LOGIN INICIAL--------------------------------------------------                   

    print("Seja bem vindo a TECA!")

    while True:
        ask = input(' Já é cadastrado? Y/N ')

        if (ask == 'Y' or ask == 'y' ):
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

 #-------------------------------------CADASTRAMENTO DO USUÁRIO--------------------------------------------------                   
     
        #-----INÍCIO DO CADASTRAMENTO INICAL DO USUARIO-----#
        if (ask == 'N' or ask == 'n'):                 
                print('Então vamos lhe cadastrar!!')          
                
                #---INICIO DA ENTRADA DA MATRICULA---#     
                while True:
                    matricula = input('> Digite sua matricula\n>>>: ') 
                    if database.Usuario.select(matricula) is None:
                        break
                    else:
                        print("Matrícula ocupada!")
                #---FIM DA ENTRADA DA MATRICULA---#        

                nome = input('>Qual o seu nome completo?\n>>>: ')
                endereco = input('>Onde você mora?\n>>>: ')    
                
                #---INICIO DA ENTRADA DO TIPO DE USUARIO---#
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
                #---INICIO DA ENTRADA DO TIPO DE USUARIO---#
                
                #---INICIO DA ENTRADA DO NICKNAME---#                                   
                while True:
                    nickname = input('>Digite um nickname para acesso a sua conta: ')
                    if len(database.Usuario.filter(nickname=nickname)) == 0 :
                        break
                    else:
                        print("Nickname já existe!") 
                senha_cadastro = getpass.getpass(prompt='>Digite uma senha: ')
                #---FIM DA ENTRADA DO TIPO DE USUARIO---#

        #-----FIM DO CADASTRAMENTO INICAL DO USUARIO-----#

                #-----INÍCIO DO CADASTRO DO ALUNO-----#
                if(tipo_usuario == '1'):   
                        
                            #---INICIO DA ENTRADA DO CÓDIGO DE CURSO---#
                            tipos_de_curso = {
                                '1':'Engenharia de Computação',
                                '2':'Engenharia Elétrica',
                                '3':'Psicologia'
                                '4':'Finanças'
                                '5':'Economia'  
                            }
                            print('>Digite o código de seu curso')
                            for numero,tipo in tipos_de_curso.items():
                                print(numero,tipo)
                            while True:
                                cod_curso = input('\n>>>: ')
                                if cod_curso in tipos_de_curso:
                                    tipo = tipos_de_usuario[cod_curso]
                                    break
                                else:
                                    print('Opção inválida')
                            #---FIM DA ENTRADA DO CÓDIGO DE CURSO---#

                            data_de_ingresso     = input('> Em que ano,mês e dia você entrou na UFC?(YYYY-MM-DD)\n>>>: ')
                            data_de_conclusao    = input('> Em que ano,mês e dia você vai concluir seu curso?(YYYY-MM-DD)\n>>>: ')
                            
                            #-----CHECK-----#
                            print('\n')
                            print('Código do curso: '+cod_curso+'\n')
                            print('Data de ingresso no curso: '+data_de_ingresso+'\n')
                            print('Data de conclusão do curso: '+data_de_conclusao+'\n')
                #-----FIM DO CADASTRO DO ALUNO-----#            

                #-----INCIO DO CADASTRO DE PROFESSOR-----#            
                if(tipo_usuario == '2'):              
                                
                            data_de_contratacao  = input('> Em que ano, mês e dia você foi contratado pela UFC?(YYYY-MM-DD)\n>>>: ')
                            
                            #---INICIO DA ENTRADA DO REGIME DE TRABALHO---#
                            tipos_regime = {
                                '1':'D.E.(Dedicação exclusiva)',
                                '2':'20 horas',
                                '3':'40 horas'
                            }
                            print('> O seu regime de trabalho é de quantas horas?\nOpções:')
                            for numero,regimes in tipos_regime.items():
                                print(numero,regimes)
                            while True:
                                regime_trb = input('\n>>>: ')
                                if regime_trb in tipos_regime:
                                    regimes = tipos_regime[regime_trb]
                                    if regime_trb == '1':
                                        regime_de_trabalho = 'DE'
                                        break
                                    if regime_trb == '2':
                                        regime_de_trabalho = '20H'
                                        break
                                    if regime_trb == '3':
                                        regime_de_trabalho = '40H'    
                                        break                                                                              
                                else: 
                                    print('Opção inválida!')
                            #---FIM DA ENTRADA DO REGIME DE TRABALHO---#        
                            
                            #---INICIO DA ENTRADA DO CÓDIGO DE CURSO---#    
                            tipos_de_curso = {
                                '1':'Engenharia de Computação',
                                '2':'Engenharia Elétrica',
                                '3':'Psicologia'
                                '4':'Finanças'
                                '5':'Economia'  
                            }
                            print('>Digite o código de seu curso')
                            for numero,tipo in tipos_de_curso.items():
                                print(numero,tipo)
                            while True:
                                cod_curso = input('\n>>>: ')
                                if cod_curso in tipos_de_curso:
                                    tipo = tipos_de_usuario[cod_curso]
                                    break
                                else:
                                    print('Opção inválida')
                            #---FIM DA ENTRADA DO CÓDIGO DE CURSO---#

                            #-----CHECK-----#                            
                            print('\n')
                            print('Data de contração: '+data_de_contratacao+'\n')
                            print('Regime de trabalho: '+regime_de_trabalho+'\n')
                            print('Código do curso: '+cod_curso+'\n')

                #-----FIM DO CADASTRO DE PROFESSOR-----#            

                #-----INICIO INSERÇÃO DOS TELEFONES-----#(BUG!!!!!)(LIMITAR O TAMANHO DO TELEFONE)                
                telefones = []   
                while True:
                    telefone = input('> Digite um numero de telefone: ')
                    telefones.append(telefone)
                    ask_2    = input('> Tem mais algum telefone?(Y/N) ')
                    if (ask_2 == 'N'):
                        break
                #-----FIM INSERÇÃO DOS TELEFONES-----#                                            
                

                confirmacao = input('Está certo dos dados o que você colocou?(Y/N):')

                #-----INICIO INSERÇÃO NO BANCO DE DADOS-----#
                if(confirmacao == 'Y' or confirmacao == 'y'):
                    database.Usuario(matricula, nickname, database.senha_hash(senha_cadastro), nome, endereco, tipo_usuario,'usuario').insert()
                    
                    for telefone in telefones:
                        database.Telefones(matricula,telefone).insert()
                    
                    if(tipo_usuario=='2'):
                        database.Professor(matricula, data_de_contratacao, regime_de_trabalho, cod_curso).insert()                      
                    
                    elif(tipo_usuario=='1'):
                        database.Aluno(matricula, data_de_conclusao, data_de_ingresso, cod_curso).insert()                
                    
                    elif(tipo_usuario=='3'):
                        database.Funcionario(matricula).insert()                
                #-----FIM INSERÇÃO NO BANCO DE DADOS-----#

                #-----FIM DA INSERÇÃO DE CADASTRO-----#
                print('USUÁRIO CADASTRADO!!')

if __name__ == '__main__':
    main()
