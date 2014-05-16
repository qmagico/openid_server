openid\_server
=============

Esta aplicação é um exemplo de provedor OpenId, para ser implementado pelas escolas que pretenderem realizar a integração via OpenId com o QMágico. Neste exemplo, foi utilizada uma biblioteca Python chamada [python-openid](https://github.com/openid/python-openid "python-openid") para se desenvolver esta aplicação [Django](https://www.djangoproject.com/ "Django").

Nesta aplicação não se utiliza banco de dados para armazenar usuários. Por se tratar de um exemplo, a autenticação é feita em memória com um simples if:

```Python
if username == 'MarRib' and password == '123456':
    request.session['username'] = 'MarRib'
```

Recomenda-se que se construa o provedor de OpenId baseado nessa implementação, porém, a implementação pode ser feita utilizando-se qualquer linguagem/biblioteca. Como parâmetro de testes, sugere-se que se teste a sua implementação do servidor com a implementação teste de consumidor disponibilizada na biblioteca [python-openid](https://github.com/openid/python-openid "python-openid").

![Diagrama de Sequencia do Fluxo](/DiagramaSequencia.png "Diagrama de Sequencia do Fluxo")

Você pode ler o Fluxo Resumido da autenticação via OpenId [aqui](https://github.com/qmagico/openid_server/blob/master/Fluxo.md "Fluxo Resumido")!

Você pode ler o Detalhamento da troca de mensagens durante o processo de autenticação [aqui](https://github.com/qmagico/openid_server/blob/master/Detalhamento.md "Detalhamento das mensagens")!
No detalhamento de troca de mensagens são especificados parâmetros de entrada e saída de cada requisição entre o browser, QMágico e Escola, exemplificando-os.