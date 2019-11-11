from flask import request, jsonify
from server import app
import os
import pandas as pd
import xlrd
import os
import datetime as dt
from dateutil.parser import parse
import time
import json

def save_file(file):
    
    ext = file.filename.split('.')
    ext = ext[-1]

    ExcelFile = pd.read_excel(file, sheet_name='Outubro')

    ExcelFile = ExcelFile.sort_values(['Empr', 'Interface', 'Elemento PEP'])
    
    if (ext not in app.config['ALLOWED_EXTENSIONS']):
        print('O arquivo não pode ser salvo, pois não tem o formato permitido')
    else:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        print('O arquivo foi salvo com sucesso')

    ValorRetorno = fechamento(ExcelFile)

    return ValorRetorno

def process():
    
    ValorRetorno = save_file(request.files['file'])
    
    return jsonify([1, 2, 3])

def fechamento(ExcelData):

    df = pd.DataFrame(ExcelData, columns=['Empr', 'CL', 'Conta', 'Valor do Montante', 'Elemento PEP', 'Chv.ref.1',
                                       'Data do Doc', 'Contrato', 'Data Lançamento', 'Denominação', 'Interface']).astype("str")

    StringLinha = ''
    ValorRetorno = {}
    BreakLoop = False

    if not os.path.exists('files/resultados/'):
        os.mkdir('files/resultados/')

    f = open('files/resultados/'+'Outubro'+'_'+'.txt', "w")

    #Começo a contar o tempo de execução
    BeginTime = time.perf_counter()
   
    Linha = 0
    for i in range(df.shape[0]):
        
        if (BreakLoop == True):
            break
        
        print('Linha ', Linha)

        if(Linha > 0):
            f.write('\n')
        
        Linha += 1
        
        for j in range(df.shape[1]):
            
            #Empresa | 1º Column
            if (j == 0):
                Empr = df.iloc[i, j]
                
                if (len(Empr) < 4): 
                    Empr = Empr.zfill(5)

                    print('Aviso: A informação de empresa está menor que 4! Empresa: ', str(Empr))

                    f.write("&SdtTexto.Add('" + Empr)
                elif(len(Empr) == 4):
                    Empr = Empr.zfill(5)

                    f.write("&SdtTexto.Add('" + Empr)
                else:
                    BreakLoop = True
                    print('Codigo da Empresa está com o tamanho errado! Tamanho: ' + str(len(Empr)))

                StringLinha += Empr
                    
            #Credito ou Debito | 2º Column
            elif(j == 1):
                CD = df.iloc[i, j]
                
                if (len(CD) == 1):
                    f.write(CD)
                else:
                    BreakLoop = True
                    print('Informação de Crédito ou Débito com tamanho errado! Tamanho: ' + str(len(CD)))

                StringLinha += CD

            #Conta | 3º Column
            elif(j == 2):
                Conta = df.iloc[i, j]
                
                if (len(Conta) == 10):
                    f.write(Conta)
                else:
                    BreakLoop = True
                    print('Informação de Conta está com tamanho errado! Tamanho: ' + str(len(Conta)))

                StringLinha += Conta

            #Valor do Montante | 4º Column
            elif(j == 3):
                ValorDoMontante = float(df.iloc[i, j])
                
                ValorDoMontante = '{0:.2f}'.format(ValorDoMontante)
                
                ValorDoMontante = str(ValorDoMontante).replace(".","").zfill(15)

                if (len(ValorDoMontante) == 15):
                    f.write(ValorDoMontante)
                else:
                    BreakLoop = True
                    print('O valor do montante está com o tamanho errado! Tamanho: ' + str(len(ValorDoMontante)))

                StringLinha += ValorDoMontante

            #PEP | 5º Column
            elif(j == 4):
                PEP = df.iloc[i, j]
                
                if (len(PEP) == 15):
                    PEP = PEP + '        '
                    f.write(PEP)
                else:
                    BreakLoop = True
                    print('A informação de PEP está com o tamanho errado! Tamanho: ' + str(len(PEP)))

                StringLinha += PEP

            #Chave Referencia | 6º Column
            elif(j == 5):
                ChaveRef = df.iloc[i, j]
                
                if (ChaveRef == 'nan'):
                    ChaveRef = '            '
                    f.write(ChaveRef)
                elif (len(ChaveRef) == 12):
                    f.write(ChaveRef)
                elif (len(ChaveRef) < 12):
                    ChaveRef = ChaveRef.ljust(12)
                    f.write(ChaveRef)
                    print('Aviso! A informação de ChaveRef está menor que 12! ChaveRef: ', str(ChaveRef))
                else:
                    BreakLoop = True
                    print('A informação de Chave Ref. está com o tamanho errado! Tamanho: ' + str(len(ChaveRef)))

                StringLinha += ChaveRef

            #Data do Documento | 7º Column      
            elif(j == 6):
                DataDoDocumento = df.iloc[i, j]
                #Atraso na velocidade da execução
                DataDoDocumento = dt.datetime.strptime(DataDoDocumento, '%Y-%m-%d').strftime('%Y%m%d')
                
                if (len(DataDoDocumento) == 8):
                    f.write(DataDoDocumento)
                else:
                    BreakLoop = True
                    print('A informação da Data do Documento está com o tamanho errado! Tamanho: ' + str(len(DataDoDocumento)))

                StringLinha += DataDoDocumento
                    
            #Contrato | 8º Column
            elif(j == 7):
                Contrato = df.iloc[i, j]
                
                if (len(Contrato) < 6):
                    print('Aviso: A informação de contrato está menor que 6 - Contrato: ', Contrato)
                    Contrato = Contrato.zfill(6)
                    f.write(Contrato)
                elif (len(Contrato) > 6):
                    BreakLoop = True
                    print('A informação de Contrato está menor que o normal! Tamanho: ', str(len(Contrato)))
                else:
                    f.write(Contrato)

                StringLinha += Contrato
            
            #Data do Lançamento | 9º Column
            elif(j == 8):
                DataDoLancamento = df.iloc[i, j]
                
                DataDoLancamento = dt.datetime.strptime(DataDoLancamento, '%Y-%m-%d').strftime('%d/%m/%Y')
                
                if (len(DataDoLancamento) == 10):
                    f.write(DataDoLancamento)
                else:
                    BreakLoop = True
                    print('A informação de Data do Lancamento está errada! Tamanho: ', str(len(DataDoLancamento)))

                StringLinha += DataDoLancamento

            #Histórico | 10º Column
            elif(j == 9):              
                Historico = df.iloc[i, j]

                QuotationMark = "')"

                if (len(Historico) > 50):
                    Historico = Historico.format(Historico, 50)

                    StringLinha += Historico

                    Historico += QuotationMark
                    print('Aviso! O tamanho da informação de historico veio maior que 50')
                elif (len(Historico) == 50):
                    StringLinha += Historico

                    Historico += QuotationMark
                else:
                    StringLinha += Historico

                    SpacesToFill = 52 - len(Historico)
                    QuotationMark = QuotationMark.rjust(SpacesToFill)
                    Historico += QuotationMark

                if (len(Historico) == 52):
                    f.write(Historico)
                else:
                    BreakLoop = True
                    print('A informação de Histórico está errada! Tamanho: ', str(len(Historico)))

            #Interface | 11º Column
            elif(j == 10):
                Interface = df.iloc[i, j]
                Empr_OriginValue = str(df.iloc[i, 0]) 

                ValorRetorno[Linha] = StringLinha 
                StringLinha = ''

                if(Linha < df.shape[0]):
                    NextInterface = str(df.iloc[i+1, j])
                    NextEmpr      = str(df.iloc[i+1, 0])
                    if(Interface != NextInterface) or (Empr_OriginValue != NextEmpr):
                        f.write("\nDo 'Processar'")
                        ValorRetorno['QuebraInterface'] = "Do 'Processar'"
                elif(Linha == df.shape[0]):
                    f.write("\nDo 'Processar'")
                    ValorRetorno['QuebraInterface'] = "Do 'Processar'"
                
    f.close()
    
    EndTime = time.perf_counter()
    ProcessTime = EndTime - BeginTime
    FormatTime = '{0:.2f}'.format(ProcessTime)

    # Mostrar os valores do dicionario | HAIL PYTHON 
    for item, valor in ValorRetorno.items():
        if item == 10:
            break
        print(item, valor)

    print('Tempo de processamento: ' + str(FormatTime) + ' segundos.')
    return ValorRetorno
