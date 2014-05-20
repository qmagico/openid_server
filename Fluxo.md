# Fluxo:
============================

![Diagrama de Sequencia do Fluxo](/images/DiagramaSequencia.png "Diagrama de Sequencia do Fluxo")

## 1.
O browser faz uma requisição para o QMágico para iniciar a autenticação via OpenId.

## 2.
O QMágico faz uma requisição para a Escola de um documento XRDS, contendo informações sobre as urls do provedor de OpenId.

## 3.
Este passo não ocorre todas as vezes:
Caso ainda não exista uma Associação pré-estabelecida, o QMágico faz uma requisição ao servidor da Escola para salvar uma Associação. Caso a resposta dessa requisição seja falsa, ao final do processo será feita uma outra requisição com a mesma finalidade. (Número 9 do fluxo).

## 4.
O QMágico, define quais informações espera da requisição que será feita a escola, no caso, somente o 'nickname'.
Além disso, o QMágico retorna ao browser um form html preenchido, jutamente com um script javascript que faz um submit deste form, assim que o browser o recebe.

## 5.
O browser envia para o servidor da escola, as informações do consumidor presentes no form gerado pelo QMágico.

## 6.
Primeiramente o servidor da Escola identifica se há ou não usuário logado na Escola, caso não haja é renderizada a tela de login, para posteriormente, após a validação do usuário, criar uma mensagem de resposta contendo as informações (no caso somente o username do QMágico) do aluno logado.

## 7.
A Escola envia para o browser a mensagem criada no passo anterior e uma url para onde o browser deve redirecionar essa mensagem no QMágico.

## 8.
O browser faz uma chamada com a url que recebeu na requisição 7, no caso '/loginopenid/complete', onde faz algumas validações das informações que está recebendo, tais como:
se a url que o retornou é a mesma a qual foi feita a requisição (no caso, '/openid')
se as informações específicas do usuário que o QMágico estava esperando são as mesmas que recebeu (no caso, 'nickname')
se as informações específicas do usuário estão de acordo com a especificação SREG

CAMPOS ACEITOS PELA ESPECIFICACAO SREG:

parameter|name
:-----------:|:--------------:
'fullname'|'Full Name'
'nickname'|'Nickname'
'dob'|'Date of Birth'
'email'|'E-mail Address'
'gender'|'Gender'
'postcode'|'Postal Code'
'country'|'Country'
'language'|'Language'
'timezone'|'Time Zone'

se o identificador do consumidor recebido pelo servidor da escola equivale ao identificador enviado (janrain\_nonce)

caso todas as validações sejam positivas, o QMágico recebe os dados específicos do aluno do servidor da Escola e loga o usuário no QMágico

## 9.
Este passo não ocorre todas as vezes:
Caso ainda não exista uma Associação pré-estabelecida, devido a uma resposta inesperada no passo 3, durante as validações no passo anterior é disparada uma nova requisição ao servidor da Escola para /openid, que deve retornar uma Associação para o QMágico prosseguir a validação.

## 10.
Caso o usuário esteja logado no QMágico, o browser é redirecionado para '/', para a tela inicial do QMágico, com o usuário logado.
