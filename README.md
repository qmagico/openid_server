openid\_server
=============

Esta aplicação é um exemplo de provedor OpenId, para ser implementado pelas escolas que pretenderem realizar a integração via OpenId com o QMágico. Neste exemplo, foi utilizada uma biblioteca Python chamada [python-openid](https://github.com/openid/python-openid "python-openid") para se desenvolver esta aplicação [Django](https://www.djangoproject.com/ "Django").

Nesta aplicação não se utiliza banco de dados para armazenar usuários. Por se tratar de um exemplo, a autenticação é feita em memória com um simples if:

```Python
if username == 'MarRib' and password == '123456':
    request.session['username'] = 'MarRib'
```

Recomenda-se que se construa o provedor de OpenId baseado nessa implementação, substituindo essa autenticação mínima por uma implementação real de banco de dados da escola, porém, a implementação pode ser feita utilizando-se qualquer linguagem/biblioteca. Como parâmetro de testes, sugere-se que se teste a sua implementação do servidor com a implementação teste de consumidor disponibilizada na biblioteca [python-openid](https://github.com/openid/python-openid "python-openid").

Para isto:

- Primeiramente deve-se ter o [Python](https://www.python.org/downloads/ "Python") instalado no seu computador.

- Em seguida, copie a biblioteca [python-openid](https://github.com/openid/python-openid "python-openid") para o seu computador:

```Shell
git clone https://github.com/openid/python-openid.git "diretorio"
```

- Para rodar o consumidor do exemplo, entre na pasta python-openid/examples/ e rode o consumidor via linha de comando:

```Shell
python consumer.py
```

- Pronto, seu consumidor deve estar rodando em http://localhost:8001, ou, caso você deseje alterar a porta, altere a linha 473 do consumer.py.

- Para testar o seu servidor OpenId, basta inserir a url que inicia a autenticação OpenId do seu servidor, neste caso, seria: http://localhost:8090/xrds (ou a porta que você desejar) e marcar o checkbox "Request registration data", como abaixo:

![Exemplo de entrada no Consumidor](/images/openid_consumer_example.png "Exemplo de entrada no Consumidor")

- Não se esqueça de conectar o seu servidor e utilizar a porta certa. No meio do processo você pode ser redirecionado para uma tela de login, feito isso, a resposta esperada do processo é uma tela como a seguinte:

![Exemplo de saída no Consumidor](/images/openid_consumer_example_result.png "Exemplo de saída no Consumidor")

Você pode entender melhor o fluxo do processo com o diagrama abaixo e a documentação adicional a seguir:

![Diagrama de Sequencia do Fluxo](/images/DiagramaSequencia.png "Diagrama de Sequencia do Fluxo")

Você pode ler o Fluxo Resumido da autenticação via OpenId [aqui](https://github.com/qmagico/openid_server/blob/master/Fluxo.md "Fluxo Resumido")!

Você pode ler o Detalhamento da troca de mensagens durante o processo de autenticação [aqui](https://github.com/qmagico/openid_server/blob/master/Detalhamento.md "Detalhamento das mensagens")!
No detalhamento de troca de mensagens são especificados parâmetros de entrada e saída de cada requisição entre o browser, QMágico e Escola, exemplificando-os.
