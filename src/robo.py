from flask import request, Response
from server import app
import os
import pandas as pd
import xlrd
import os
import datetime as dt
from dateutil.parser import parse
import time
import base64
from dict2xml import dict2xml as xmlify
import json

def process_file(file):

    try:
        ExcelFile = pd.read_excel(file, sheet_name=request.form['aba'])
    except:
        return('A planilha desejada não foi encontrada')

    ExcelFile = ExcelFile.sort_values(['Empr', 'Interface', 'Elemento PEP'])
    
    ValorRetorno = fechamento(ExcelFile)

    return ValorRetorno

def process():
    
    retorno = process_file(request.files['file'])

    retorno = json.dumps(retorno)

    file = open('files/teste.json', 'w')
    
    file.write(retorno)
        
    return Response(retorno, mimetype='application/json')

def fechamento(ExcelData):

    df = pd.DataFrame(ExcelData, columns=['Empr', 'CL', 'Conta', 'Valor do Montante', 'Elemento PEP', 'Chv.ref.1',
                                       'Data do Doc', 'Contrato', 'Data Lançamento', 'Denominação', 'Interface']).astype("str")

    StringLinha = ''
    ValorRetorno = {}
    avisos = {}
    erros = {}
    texto_formatado = {}
    BreakLoop = False

    #Começo a contar o tempo de execução
    BeginTime = time.perf_counter()
   
    Linha = 0
    for i in range(df.shape[0]):
        
        if (BreakLoop == True):
            break
        
        print('Linha ', Linha)
        
        Linha += 1
        
        for j in range(df.shape[1]):
            
            #Empresa | 1º Column
            if (j == 0):
                Empr = df.iloc[i, j]
                
                if (len(Empr) < 4): 
                    Empr = Empr.zfill(5)

                    avisos[Linha] = ('A informação de empresa está menor que 4! Empresa: ', str(Empr))

                elif(len(Empr) == 4):
                    Empr = Empr.zfill(5)

                else:
                    BreakLoop = True
                    erros[Linha] = ('Codigo da Empresa está com o tamanho errado! Tamanho: ' + str(len(Empr)))

                StringLinha += Empr
                    
            #Credito ou Debito | 2º Column
            elif(j == 1):
                CD = df.iloc[i, j]
                
                if (len(CD) != 1):
                    BreakLoop = True
                    erros[Linha] = ('Informação de Crédito ou Débito com tamanho errado! Tamanho: ' + str(len(CD)))

                StringLinha += CD

            #Conta | 3º Column
            elif(j == 2):
                Conta = df.iloc[i, j]
                
                if (len(Conta) != 10):
                    BreakLoop = True
                    erros[Linha] = ('Informação de Conta está com tamanho errado! Tamanho: ' + str(len(Conta)))

                StringLinha += Conta

            #Valor do Montante | 4º Column
            elif(j == 3):
                ValorDoMontante = float(df.iloc[i, j])
                
                ValorDoMontante = '{0:.2f}'.format(ValorDoMontante)
                
                ValorDoMontante = str(ValorDoMontante).replace(".","").zfill(15)

                if (len(ValorDoMontante) != 15):
                    BreakLoop = True
                    erros[Linha] = ('O valor do montante está com o tamanho errado! Tamanho: ' + str(len(ValorDoMontante)))
                
                StringLinha += ValorDoMontante

            #PEP | 5º Column
            elif(j == 4):
                PEP = df.iloc[i, j]
                
                if (len(PEP) == 15):
                    PEP += '        '
                else:
                    BreakLoop = True
                    erros[Linha] = ('A informação de PEP está com o tamanho errado! Tamanho: ' + str(len(PEP)))

                StringLinha += PEP

            #Chave Referencia | 6º Column
            elif(j == 5):
                ChaveRef = df.iloc[i, j]
                
                if (ChaveRef == 'nan'):
                    ChaveRef = '            '
                    StringLinha += ChaveRef
                elif (len(ChaveRef) == 12):
                    StringLinha += ChaveRef
                elif (len(ChaveRef) < 12):
                    ChaveRef = ChaveRef.ljust(12)
                    StringLinha += ChaveRef
                    avisos[Linha] = ('Aviso! A informação de ChaveRef está menor que 12! ChaveRef: ', str(ChaveRef))
                else:
                    StringLinha += ChaveRef
                    BreakLoop = True
                    erros[Linha] = ('A informação de Chave Ref. está com o tamanho errado! Tamanho: ' + str(len(ChaveRef)))
                
            #Data do Documento | 7º Column      
            elif(j == 6):
                DataDoDocumento = df.iloc[i, j]
                #Atraso na velocidade da execução
                DataDoDocumento = dt.datetime.strptime(DataDoDocumento, '%Y-%m-%d').strftime('%Y%m%d')
                
                if (len(DataDoDocumento) != 8):
                    BreakLoop = True
                    erros[Linha] = ('A informação da Data do Documento está com o tamanho errado! Tamanho: ' + str(len(DataDoDocumento)))

                StringLinha += DataDoDocumento
                    
            #Contrato | 8º Column
            elif(j == 7):
                Contrato = df.iloc[i, j]
                
                if (len(Contrato) < 6):
                    avisos[Linha] = ('Aviso: A informação de contrato está menor que 6 - Contrato: ' + Contrato)
                    Contrato = Contrato.zfill(6)
                    StringLinha += Contrato
                elif (len(Contrato) > 6):
                    StringLinha += Contrato
                    BreakLoop = True
                    erros[Linha] = ('A informação de Contrato está menor que o normal! Tamanho: ' + len(Contrato))
                else:
                    StringLinha += Contrato

            #Data do Lançamento | 9º Column
            elif(j == 8):
                DataDoLancamento = df.iloc[i, j]
                
                DataDoLancamento = dt.datetime.strptime(DataDoLancamento, '%Y-%m-%d').strftime('%d/%m/%Y')
                
                if (len(DataDoLancamento) != 10):
                    BreakLoop = True
                    erros[Linha] = ('A informação de Data do Lancamento está errada! Tamanho: ' + str(len(DataDoLancamento)))
                
                StringLinha += DataDoLancamento

            #Histórico | 10º Column
            elif(j == 9):              
                Historico = df.iloc[i, j]

                if (len(Historico) > 50):
                    Historico = Historico.format(Historico, 50)

                    StringLinha += Historico
                    avisos[Linha] = ('Aviso! O tamanho da informação de historico veio maior que 50')

                elif (len(Historico) < 50):
                    SpacesToFill = 50 - len(Historico)
                    Historico += ' ' * SpacesToFill
                    StringLinha += Historico
                
                elif (len(Historico) == 50):
                    StringLinha += Historico
                
                else:
                    avisos[Linha] = ('Aviso! O tamanho da informação de historico está com tamanho errado: ' + 
                            'Empresa:' + Empr + 'Contrato:' + Contrato + 'Historico:' + Historico)

            #Interface | 11º Column
            elif(j == 10):
                Interface = df.iloc[i, j]
                Empr_OriginValue = str(df.iloc[i, 0]) 
                
                texto_formatado[Linha] = StringLinha
                StringLinha = ''

                if(Linha < df.shape[0]):
                    NextInterface = str(df.iloc[i+1, j])
                    NextEmpr      = str(df.iloc[i+1, 0])
                    if(Interface != NextInterface) or (Empr_OriginValue != NextEmpr):
                        Linha += 1
                        texto_formatado[Linha] = "Do 'Processar'"
                elif(Linha == df.shape[0]):
                    Linha += 1
                    texto_formatado[Linha] = "Do 'Processar'"
    
    EndTime = time.perf_counter()
    ProcessTime = EndTime - BeginTime
    FormatTime = '{0:.2f}'.format(ProcessTime)

    # Visualizando os valores do ValorRetorno
    count = 0
    for chave, valor in ValorRetorno.items():
        if count == 10:
            print(chave, valor)
            break
        else:
            print(chave, valor)
            count += 1
    
    print('Tempo de processamento: ' + str(FormatTime) + ' segundos.')

    ValorRetorno['texto_formatado']  = texto_formatado
    ValorRetorno['avisos'] = avisos
    ValorRetorno['erros'] = erros

    return ValorRetorno