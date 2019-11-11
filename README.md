# Formatação de valores em Excel para arquivo texto usando WebService com Python

Esse é um projeto de automação com Python para o fechamento contábil de uma empresa. A princípio, o fechamento era feito manualmente editando uma 
planilha em Excel formatando os valores para um arquivo em .txt de acordo com as regras impostas, depois foi utilizado um script em Python para fazer 
com que o processo de fechamento seja automatizado. 

O script passou por várias modificações para que fosse otimizado, e agora está sendo desenvolvido uma WebService para facilitar ainda mais o processo.

## Principais Tecnologias Utilizadas:
* Python 3.7.x                    
* Flask                           
* Pip                             
* Virtualenv       
  
## Motivo
Antes o processo era feito manualmente e demandava muito tempo para ser feito, além de a validação não ser muito assertiva.
A automatização do processo em Python melhorou a demanda de tempo de 2 horas para 10 segundos somente na formatação do texto
em uma planilha com 16 mil linhas como exemplo.

Com o WebService oferecendo esse processo, o motivo é facilitar o acesso de outras ferramentas utilizadas pela empresa.

## Como funciona
É enviado uma planilha para o WebService, é processado formatando os valores das colunas respeitando as regras e será retornado
os valores formatados para a validação e aplicação em banco de dados.
  
 ## Lembre-se 
 Antes de instalar as dependências necessárias crie um ambiente virtual, isso ajuda muito na separação de pacotes e instalação.
 
 O arquivo requirements.txt contém todas as dependências que o projeto precisa para funcionar.
 Para instalar essas dependências utilize o comando: 
 ```python 
pip install -r requirements.txt
```
