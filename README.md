# Formatação de valores em Excel para arquivo texto usando WebService com Python

Esse é um projeto de automação com Python para o fechamento contábil de uma empresa. A princípio, o fechamento era feito manualmente editando uma 
planilha em Excel formatando os valores para um arquivo em .txt de acordo com as regras impostas, depois foi utilizado um script em Python para fazer 
com que o processo de fechamento seja automatizado. 

O script passou por várias modificações para que fosse otimizado, e agora foi desenvolvido um WebService para a disponibilização desse serviço.

## Principais Tecnologias Utilizadas:
* Python 3.7.x                    
* Flask                           
* Pip                             
* Virtualenv
* Pandas
* Axios
  
## Motivo
Antes o processo era feito manualmente e demandava muito tempo para ser feito, além de a validação não ser muito assertiva.
A automatização do processo em Python melhorou a demanda de tempo de 2 horas para 10 segundos somente na formatação do texto
em uma planilha com 16 mil linhas como exemplo.

Com o WebService oferecendo esse processo, o motivo é facilitar o acesso de outras ferramentas utilizadas pela empresa.

## Como funciona
O WebService recebe dois parâmetros de entrada:
* *Aba* - Que é o nome da aba da planilha a ser processada.
* *File* - Que é a planilha a ser processada.

As informações são enviadas para a rota */fechamento* onde é verificado as informações enviadas e o processo é inicializado.

## Testes

Para testes é necessario executar o comando abaixo:
```python
python .\run.py
```
que irá inicializar o servidor local pelo implantado pelo *Flask*.

Foi criado o arquivo *index.html* para a requisição *POST* em *JS* e *Axios*, no arquivo é informado as duas chaves de parâmetros,
e o método pode ser executado pelo botão *POST*

A porta como padrão está como *5000*, portando para programas de testes de requisições (*Postman*, *Insomnia*, etc.) é necessário
colocar na URL o link *http://localhost:5000/fechamento* e especificar o método *POST*.
  
 ## Lembre-se 
 Antes de instalar as dependências necessárias crie um ambiente virtual, isso ajuda muito na separação de pacotes e instalação.
 
 O arquivo requirements.txt contém todas as dependências que o projeto precisa para funcionar.
 Para instalar essas dependências utilize o comando: 
 ```python 
pip install -r requirements.txt
```
