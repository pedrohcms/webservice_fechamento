import json
from flask import Response

ValorRetorno   = {}

Erros          = []
Avisos         = []
TextoFormatado = []

for i in range(10):
    Erros.append('Linha: ' + str(i))

for i in range(5):
    Avisos.append(str(i))

for i in range(15):
    TextoFormatado.append(str(i))

ValorRetorno['erros']           = Erros
ValorRetorno['avisos']          = Avisos
ValorRetorno['texto_formatado'] = TextoFormatado

ValorRetornoJson = json.dumps(ValorRetorno)

print(ValorRetornoJson)

