ValorRetorno   = []

Erros          = []
Avisos         = []
TextoFormatado = []

for i in range(10):
    Erros.append('chave')
    Erros.append(str(i))

for i in range(5):
    Avisos.append('chave')
    Avisos.append(str(i))

for i in range(15):
    TextoFormatado.append('chave')
    TextoFormatado.append(str(i))

ValorRetorno.append(Erros)
ValorRetorno.append(Avisos)
ValorRetorno.append(TextoFormatado)

def ListToDict(List):
    Dict = {List[i]: List[i + 1] for i in range(0, len(List), 2)}
    return Dict

Erros_Dicionario = ListToDict(Erros)

for valor in Erros:
    print(valor)

print('\n Dicionario agora porra: ')

for chave, valor in Erros_Dicionario.items():
    print(chave, valor)
