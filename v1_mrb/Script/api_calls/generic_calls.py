#import http.client
#import mimetypes
#from codecs import encode

"""
  Gestisce le chiamate API con aqHttp
  @param method: HTTP method
  @param url: request url
  @param token: Authorization Header Bearer token
  @param path: endpoint path, solo per logging (esempio: /contracts)
  @param body opzionale
"""
def send_request_generic(method, url, token, path, body=None):
  try:     
    # Creo la request
    aqHttpRequest = aqHttp.CreateRequest(method, url)
    aqHttpRequest.SetTimeouts(0, 60000, 120000, 120000)
    # Setto gli header
    aqHttpRequest.SetHeader("Authorization", "Bearer "+token)
    # Invio la request e salvo la response nell'oggetto aqHttpResponse
    if body == None:
      aqHttpResponse = aqHttpRequest.Send()
    else: 
      aqHttpRequest.SetHeader("Content-Type", "application/json")
      aqHttpResponse = aqHttpRequest.Send(body)

    if aqHttpResponse == None:
      Log.Error('Il servizio '+path+' non ha risposto')
      
    Log.Message('Il servizio '+path+' ha risposto con status: '+str(aqHttpResponse.StatusCode)+' '+aqHttpResponse.StatusText)
    
    return aqHttpResponse
      
  except RuntimeError as e:
    Log.Error('Errore di runtime: '+str(e))
  except Exception as ex:
    Log.Error('Errore generico: '+str(ex))

       
#"""
#  Esegue una chiamata post multipart/formdata di un file usando http.client
#  (- sintassi ottenuta da code snippet postman)
#  @param host: 
#  @param path:
#  @param file_path:
#  @param file_name:
#  @param token:
#"""    
#def post_multipart_formdata_file(host, path, file_path, file_name, token):  
#  try:
#    ## Creo una connessione HTTPS al server specificato 
#    conn = http.client.HTTPSConnection(host)
#    
#    dataList = []
#    ## Il boundary è una stringa che separa le parti del contenuto multipart/form-data
#    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
#    
#    ## Cosruisco la parte multipart
#    dataList.append(encode('--' + boundary))
#    dataList.append(encode('Content-Disposition: form-data; name=multipartFile; filename={0}'.format(file_name)))
#
#    ## Determino il tipo MIME del file (es. image/png, application/pdf ec...)
#    fileType = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
#    dataList.append(encode('Content-Type: {}'.format(fileType)))
#    dataList.append(encode(''))
#
#    ## Apro il file in modalità binaria e lo aggiungo al corpo della richiesta 
#    with open(file_path, 'rb') as f:
#      dataList.append(f.read())
#    dataList.append(encode('--'+boundary+'--'))
#    dataList.append(encode(''))
#    body = b'\r\n'.join(dataList)
#    payload = body
#
#    ## Imposto tutti gli header
#    headers = {
#      'authorization': 'Bearer '+token,
#      'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
#    }
#    
#    ## Invio la POST e leggo la risposta
#    conn.request("POST", path, payload, headers)
#    res = conn.getresponse()
#    data = res.read()
#    body = data.decode("utf-8")
#    
#    ## Gestione della response
#    if data == None:
#      Log.Error('Il servizio '+path+' non ha risposto')
#    else:
#      Log.Message('Il servizio '+path+' ha risposto con status: '+str(res.status)+' '+res.reason)
#      response_obj = { 'http_status_code': res.status, 'http_status_message': res.reason }
#    
#    ## Se il servizio ha risposto OK o CREATED, verifico che il body contenga un numero intero, ossia l'id della risorsa, eseguendo un casting da str (utf-8) ad int e gestendo l'errore ##
#    if res.status == 200 or res.status == 201:
#      try:
#        int(body)
#        response_obj.update({ 'body': body })
#        return response_obj
#      except Exception as e:
#        Log.Error('Il servizio ha risposto 200 OK o 201 CREATED ma non è stato restituito un numero intero (id della risorsa) nel body')
#    else:
#      return response_obj
#    
#  except RuntimeError as e:
#    Log.Error('Errore di runtime: '+str(e))
#  except Exception as ex:
#    Log.Error('Errore generico: '+str(ex))
