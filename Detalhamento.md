Detalhamento
=============

![Diagrama de Sequencia do Fluxo](/DiagramaSequencia.png "Diagrama de Sequencia do Fluxo")

# Detalhamento do Fluxo:

## 1. e 4. /loginopenid/start?provider=x
- Requestor: Browser

- method: GET 
- parametros:

provider: string que identifica o servidor ao qual o QMágico irá se comunicar para obter as informações do usuário

- HEADER: None

Resposta:
- Status:200
- Paramêtros: Null
- Body: Form como o abaixo, que ao ser retornado ao browser, enviará resposta ao seu 'action', no caso: 'http://www.openid_server.com/openid', a Escola.

```HTML
<html>
<head>
  <title>OpenID transaction in progress</title>
</head>
<body onload="document.forms[0].submit();">
	<form id="openid_message" action="http://www.openid_server.com/openid" method="post" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded">
		<input name="openid.realm" type="hidden" value="http://www.namespace.qmagico.com.br"/>
		<input name="openid.mode" type="hidden" value="checkid_setup"/>
		<input name="openid.identity" type="hidden" value="http://www.openid_server.com/xrds"/>

		<input name="openid.assoc_handle" type="hidden" value="{HMAC-SHA1}{5373dec2}{L5fY7A==}"/>

		<input name="openid.return_to" type="hidden" value="http://www.namespace.qmagico.com.br/loginopenid/complete?janrain\_nonce=2014-05-14T21%3A19%3A09ZdQl2o0"/>
		<input name="openid.ns.sreg" type="hidden" value="http://openid.net/extensions/sreg/1.1"/>
		<input name="openid.sreg.optional" type="hidden" value="fullname,email"/>
		<input name="openid.ns" type="hidden" value="http://specs.openid.net/auth/2.0"/>
		<input name="openid.sreg.required" type="hidden" value="nickname"/>
		<input name="openid.claimed_id" type="hidden" value="http://www.openid_server.com/xrds"/>
		<input type="submit" value="Continue"/>
	</form>
<script>
	var elements = document.forms[0].elements;
	for (var i = 0; i < elements.length; i++) {
	  elements[i].style.display = "none";
	}
</script>
</body>
</html>
```


## 2./xrds
- Requestor: QMágico (backend)

- method: GET
- parametros: None

- HEADER: None

Resposta:
- Status: 200
- Content\_type: 'application/xrds+xml'
- Body: Documento XRDS com as especificações do servidor, como o que segue:

```XML
<xrds:XRDS xmlns:xrds="xri://$xrds" xmlns="xri://$xrd*($v*2.0)">
  <XRD>

    <Service priority="0">
      <Type>http://specs.openid.net/auth/2.0/signon</Type>
      <Type>http://openid.net/signon/1.0</Type>
      <URI>http://www.openid_server.com/openid</URI>
    </Service>

  </XRD>
</xrds:XRDS>
```

## 3./openid
Caso ainda não exista uma 'Association' pré-estabelecida, o QMágico faz uma requisição ao servidor da Escola para montar uma 'Association', um dos parametros lançados nesta requisição é: "openid.mode" = 'association', o processo continua independente da resposta desta requisição ter sido positiva ou negativa, ao final do processo, será feita uma outra requisição caso ainda não se tenha uma 'Association'. (Número 9 do fluxo)

- Requestor: QMágico (backend)
- method: POST

parametro | exemplo
:---------:|:----------------
u'openid.session\_type'| u'DH-SHA1' 
u'openid.mode'| u'associate'
u'openid.dh\_consumer\_public'| u'AKFel/ucgP/LMGfeMJuEA/vs0WsR+7EnTWqrmbHnu/+BeOgFIpTEHcX79IPeBMPV2bc7uNZ6vOt2Q4DwM0XxUbrWIi9VQZwCoCStuTLe+eOr5BFnkugs0YFhYlVOyN6/bwzk/qAncA1kGSlHJuszchIUJN5FXmli1vlZgKSTUIcv'
u'openid.assoc\_type'| u'HMAC-SHA1'
u'openid.ns'| u'http://specs.openid.net/auth/2.0'

- HEADER:None

Resposta:
- Status: 200
- Parâmetros: None

- Body:

'assoc\_handle:{HMAC-SHA1}{537506f9}{3DCF/A==}
assoc\_type:HMAC-SHA1
dh\_server\_public:AMdRWv12gZpz9Vxw5bcm79iQOiHTk3aHtRUE0QXvYK5oFE8AnQINXQXhCewurG6yZznf+/wdo39kJczwGeHkyksJwxTGRTyR9u6bAijKHoHBGi2wnOMi6GAcGoc7ggA4dFh50AEyPV7Xwif/oLBefPt3duplpGRkCMl29wHYL5MY
enc\_mac\_key:nfRPJ0+TSQb2/C70qr+U9wIRBGY=
expires\_in:1209600
ns:http://specs.openid.net/auth/2.0
session\_type:DH-SHA1
'

## 5. /openid
Caso o usuário não esteja logado, as informações do POST são salvas para serem usadas na próxima requisição e uma tela de login deve ser apresentada ao usuário, que, após logado, será redirecionado para /openid novamente (requisição número 6 do fluxo), caso o usuário já esteja logado, o fluxo não passa por este número 5.
- Requestor: Browser

- method: POST

parametro | exemplo
:----------------:|:--------------------
u'openid.claimed\_id'| u'http://www.openid_server.com/xrds'
u'openid.identity'|| u'http://www.openid_server.com/xrds'
u'openid.mode'| u'checkid\_setup'
u'openid.ns'| u'http://specs.openid.net/auth/2.0'
u'openid.ns.sreg'| u'http://openid.net/extensions/sreg/1.1'
u'openid.realm'| u'http://www.namespace.qmagico.com.br'
u'openid.return\_to'| u'http://www.namespace.qmagico.com.br/loginopenid/complete?janrain_nonce=2014-05-15T18%3A16%3A01ZRtjFd7'
u'openid.sreg.optional'| u'fullname,email'
u'openid.sreg.required'| u'nickname'

- HEADER:None

Resposta:
- Status:200
- Paramêtros: 'next':'/openid'
- Body: template de login, no caso, login.html

## 6 e 7. /openid
Caso o usuário não esteja logado, as informações do POST são salvas para serem usadas na próxima requisição e uma tela de login deve ser apresentada ao usuário, que, após logado, será redirecionado para /openid novamente (requisição número 6 do fluxo), caso o usuário já esteja logado, o fluxo não passa por este número 5.

- Requestor: Browser

- method: POST

parametro | exemplo
:----------------:|:--------------------
u'openid.claimed\_id'| u'http://www.openid_server.com/xrds'
u'openid.identity'| u'http://www.openid_server.com/xrds'
u'openid.mode'| u'checkid\_setup'
u'openid.ns'| u'http://specs.openid.net/auth/2.0'
u'openid.ns.sreg'| u'http://openid.net/extensions/sreg/1.1'
u'openid.realm'| u'http://www.namespace.qmagico.com.br'
u'openid.return\_to'| u'http://www.namespace.qmagico.com.br/loginopenid/complete?janrain_nonce=2014-05-15T18%3A16%3A01ZRtjFd7'
u'openid.sreg.optional'| u'fullname,email'
u'openid.sreg.required'| u'nickname'

- HEADER:None

Resposta:
- Status:302

parametro | exemplo
:----------------:|:--------------------
'janrain\_nonce'| '2014-05-15T18%3A16%3A01ZRtjFd7'
'openid.assoc\_handle'| '%7BHMAC-SHA1%7D%7B53750e82%7D%7BW4WfyA%3D%3D%7D'
'openid.claimed\_id'| 'http%3A%2F%2Fwww.openid\_server.com%2Fxrds'
'openid.identity'| 'http%3A%2F%2Fwww.openid\_server.com%2Fxrds'
'openid.mode'| 'id\_res'
'openid.ns'| 'http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
'openid.ns.sreg'| 'http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1'
'openid.op\_endpoint'| 'http%3A%2F%2Fwww.openid\_server.com%2Fopenid'
'openid.response\_nonce'| '2014-05-15T18%3A59%3A14Zsi1GzB'
'openid.return\_to'| 'http%3A%2F%2Fwww.namespace.qmagico.com.br%2Floginopenid%2Fcomplete%3Fjanrain\_nonce%3D2014-05-15T18%253A16%253A01ZRtjFd7'
'openid.sig'| 'NzTkAtz6WSqkxFZ%2BIxtRqoUirzg%3D'
'openid.signed'| 'assoc\_handle%2Cclaimed\_id%2Cidentity%2Cmode%2Cns%2Cns.sreg%2Cop\_endpoint%2Cresponse\_nonce%2Creturn\_to%2Csigned%2Csreg.nickname'
'openid.sreg.nickname'| 'MarRib'

- Body: redirect para QMagico em: /loginopenid/complete


## 8. /loginopenid/complete
- Requestor: Browser

- method: GET 

parametro | exemplo
:----------------:|:--------------------
u'openid.return\_to'| u'http://localhost:8080/loginopenid/complete?janrain\_nonce=2014-05-15T18%3A16%3A01ZRtjFd7'
u'openid.op\_endpoint'| u'http://localhost:8090/openid'
u'openid.ns'| u'http://specs.openid.net/auth/2.0'
u'openid.ns.sreg'| u'http://openid.net/extensions/sreg/1.1'
u'openid.sig'| u'NzTkAtz6WSqkxFZ+IxtRqoUirzg='
u'openid.sreg.nickname'| u'MarRib'
u'openid.claimed\_id'| u'http://localhost:8090/xrds'
u'openid.assoc\_handle'| u'{HMAC-SHA1}{53750e82}{W4WfyA==}'
u'openid.mode'| u'id\_res'
u'openid.response\_nonce'| u'2014-05-15T18:59:14Zsi1GzB'
u'openid.identity'| u'http://localhost:8090/xrds'
u'janrain\_nonce'| u'2014-05-15T18:16:01ZRtjFd7'
u'openid.signed'| u'assoc\_handle,claimed\_id,identity,mode,ns,ns.sreg,op\_endpoint,response\_nonce,return\_to,signed,sreg.nickname'

- HEADER:None

Resposta:
- Status: 302
- Parametros: None

- Body: redirect para QMagico em: /

## 9. /openid
- Requestor: QMágico

- method: POST

parametro | exemplo
:----------------:|:--------------------
u'janrain\_nonce'| u'2014-05-15T18:16:01ZRtjFd7'
u'openid.assoc\_handle'| u'{HMAC-SHA1}{53750e82}{W4WfyA==}'
u'openid.claimed\_id'| u'http://localhost:8090/xrds'
u'openid.identity'| u'http://localhost:8090/xrds'
u'openid.mode'| u'check\_authentication'
u'openid.ns'| u'http://specs.openid.net/auth/2.0'
u'openid.ns.sreg'| u'http://openid.net/extensions/sreg/1.1'
u'openid.op\_endpoint'| u'http://localhost:8090/openid'
u'openid.response\_nonce'| u'2014-05-15T18:59:14Zsi1GzB'
u'openid.return\_to'| u'http://localhost:8080/loginopenid/complete?janrain\_nonce=2014-05-15T18%3A16%3A01ZRtjFd7'
u'openid.sig'| u'NzTkAtz6WSqkxFZ+IxtRqoUirzg='
u'openid.signed'| u'assoc\_handle,claimed\_id,identity,mode,ns,ns.sreg,op\_endpoint,response\_nonce,return\_to,signed,sreg.nickname'
u'openid.sreg.nickname'| u'MarRib'

- HEADER:None

Resposta:
- Status: 200
- Parametros: None

- Body: 
'is\_valid:true
ns:http://specs.openid.net/auth/2.0
'