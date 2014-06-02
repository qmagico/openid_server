# coding: utf-8
from email.charset import add_alias
import time

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from openid.consumer import discover
from openid.server import server
from openid.extensions import sreg, ax


# Create your views here.

from django.http import HttpResponse
from openid.store.filestore import FileOpenIDStore

def addAttributeExchangeResponse(oidrequest, response, request):
    ax_req = ax.FetchRequest.fromOpenIDRequest(oidrequest)
    if ax_req:
        required = ax_req.getRequiredAttrs()
        if len(required) == 1 and 'http://axschema.org/contact/email' in required:
            ax_resp = ax.FetchResponse(request=ax_req)
            ax_resp.addValue('http://axschema.org/contact/email', request.session['email'])
            response.addExtension(ax_resp)



def addSRegResponse(oidrequest, response, request):
    sreg_req = sreg.SRegRequest.fromOpenIDRequest(oidrequest)


    # CAMPOS ACEITOS PELA ESPECIFICACAO SREG:
        # 'fullname':'Full Name',
        # 'nickname':'Nickname',
        # 'dob':'Date of Birth',
        # 'email':'E-mail Address',
        # 'gender':'Gender',
        # 'postcode':'Postal Code',
        # 'country':'Country',
        # 'language':'Language',
        # 'timezone':'Time Zone',
    sreg_data = {
        'nickname':request.session['username']
        }

    sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, sreg_data)
    response.addExtension(sreg_resp)


@csrf_exempt
def openid(request):
    # NECESSARIAMENTE OS 3 TRECHOS DE CÓDIGO DEVEM ESTAR NESSA MESMA URL POIS O CONSUMIDOR FAZ A VERIFICACAO
    # SE A URL QUE O RESPONDER EH A MESMA URL A QUAL ELE FEZ REQUISICAO, ENTAO OS RENDERS ABAIXO NAO PODEM TROCAR DE URL
    oidserver = server.Server(FileOpenIDStore('/tmp/openid_session_store_server'), 'http://localhost:8090/openid')
    # TRECHO 1
    # NESSE TRECHO DE CODIGO SE CRIA A ASSOCIACAO NECESSARIA NA PRIMEIRA INTERACAO COM O SERVIDOR
    # ESTA ASSOCIACAO COMPOE O PARAMETRO ASSOC_HANDLE NO PRIMEIRO FORM MONTADO PELO CONSUMIDOR
    if 'openid.mode' in request.POST:
        if request.POST['openid.mode'] in ['associate', 'check_authentication']:
            oidrequest = oidserver.decodeRequest(request.POST)
            oidresponse = oidserver.handleRequest(oidrequest)
            webresponse = oidserver.encodeResponse(oidresponse)
            return HttpResponse(webresponse.body)

    # TRECHO 2
    # CASO O USUARIO NAO ESTEJA LOGADO RENDERIZA A TELA DE LOGIN
    # DEPOIS REDIRECIONA DE VOLTA PARA ESSA MESMA URL QUE A TRATA NOVAMENTE
    if not request.session.get('username', False):
        request.session['save_post'] = request.POST
        return render(request, 'login.html', {'next':'/openid'})

    # TRECHO 3
    # NESSE TRECHO DE CODIGO O SERVIDOR ASSOCIA DADOS DO USUÁRIO NO OBJETO RESPONSE E MANDA AO CONSUMIDOR
    if request.session.get('save_post', False):
        saved_post_data = request.session['save_post']
        del request.session['save_post']
    else:
        saved_post_data = request.POST
    openid_request = oidserver.decodeRequest(saved_post_data)
    openid_response = openid_request.answer(True, identity=None)
    # addSRegResponse(openid_request, openid_response, request) # PROTOCOLO SREG
    addAttributeExchangeResponse(openid_request, openid_response, request)
    webresponse = oidserver.encodeResponse(openid_response)
    # MONTA A URL COM QUERY STRING PARA REDIRECIONAR OS DADOS PARA O CONSUMIDOR
    location = None
    for header, value in webresponse.headers.iteritems():
        if header == 'location':
            location = value

    return redirect(location)

def loginform(request):
    # TELA BASICA DE LOGIN
    # CASO O USUARIO JA ESTEJA LOGADO SIMPLESMENTE IDENTIFICA O USUARIO LOGADO E DA A OPCAO DE DESLOGAR
    if request.session.get('username', False):
        username = request.session['username']
        return render(request, 'login.html', {'logged':True, 'name':username})
    else:
        return render(request, 'login.html', {'logged':False})

def login(request):
    # METODO QUE FAZ LOGIN, SALVA O USUARIO NA SESSAO CASO AS INFORMACOES DE LOGIN SEJAM COERENTES
    # NO CASO O UNICO 'USUARIO' ESTA MOCKADO FORA DE UM BANCO, SERIA USER:'MarRib' E PASS:'123456'
    username = request.POST['username']
    password = request.POST['password']
    if username == 'MarRib' and password == '123456':
        request.session['username'] = 'MarRib'
        request.session['email'] = u'''marrib@mar.ri'''
        if request.POST.get('next', False):
            next = request.POST['next']
            if next:
                return redirect(next)
        return redirect('/')
    else:
        return render(request, 'login.html', {'logged':False, 'error':'O nome de usuário e login não são compatíveis.'})

def logout(request):
    # METODO QUE FAZ LOGOUT, TIRA O USUARIO DA SESSAO E REDIRECIONA PRA TELA DE LOGIN
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('/loginform')

def xrds(request):
    # MONTA O DOCUMENTO XRDS PARA O CONSUMIDOR
    endpoint_url = 'http://' + request.environ['HTTP_HOST'] + '/openid'
    xrds_doc = """\
<?xml version="1.0" encoding="UTF-8"?>
<xrds:XRDS
    xmlns:xrds="xri://$xrds"
    xmlns="xri://$xrd*($v*2.0)">
  <XRD>

    <Service priority="0">
      <Type>%s</Type>
      <Type>%s</Type>
      <URI>%s</URI>
    </Service>

  </XRD>
</xrds:XRDS>
    """%(discover.OPENID_2_0_TYPE, discover.OPENID_1_0_TYPE, endpoint_url)
    return HttpResponse(xrds_doc, content_type='application/xrds+xml')