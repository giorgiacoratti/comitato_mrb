## Descrizione: Lanciare POST /v1/mrb/general-binding-directives/create con request body GeneralBindingDirectiveDto
## Risultato atteso: 200 OK con response body GeneralBindingDirectiveDto

## Descrizione: Crea la direttiva di binding generale

import utils, constants, json, general, general_response_schemas

expected_status_code = constants.OK_200

def TC0003_POST_CreateGenBindingDirective():
  
  ## Estraggo il body dal file .json e lo converto in obj per verificarne il formato 
  Log.Message('--- STEP 0: Recupero il body dalla GET ---')
  
  # Carico il body completo dalla Project Variable
  body_obj = json.loads(Project.Variables.ResponseBody_General)
  
  ## Rimuovo la chiave 'id' se esiste
  if "id" in body_obj:
    del body_obj["id"]
      
  Project.Variables.New_ResponseBody_General = json.dumps(body_obj, default=str)
  
  # 🔸 Log per controllo
  Log.Message("Body_General salvato: " + json.dumps(body_obj, indent=4, default=str))
  
  Log.Message("Body recuperato: " + json.dumps(body_obj, indent=4))
  
  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = general.POST_create_general(body_obj)
  
  ## Verifico e leggo lo status code 
  if resp.StatusCode != expected_status_code:
    if resp.Text != '':
      Log.Warning('Messaggio di errore: '+resp.Text)
    Log.Error('Response status NON CORRETTO. Lo status PREVISTO era: '+str(expected_status_code))
  else:
    Log.Message('Response status CORRETTO.')
    
    ## Verifico la response validandola contro lo schema atteso 
    ## Se sono presenti dati li salvo in variabili locali e li loggo 
    Log.Message('--- STEP 2: Validazione della response')
    
    if resp.Text == '':
      Log.Error('La response non contiene un body')
    else:
      response_body_dict = json.loads(resp.Text)
    
      schema = general_response_schemas.GeneralBindingDirectiveDto
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso GeneralBindingDirectiveDto')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))