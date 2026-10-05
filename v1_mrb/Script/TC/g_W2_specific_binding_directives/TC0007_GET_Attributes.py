## Descrizione: Lanciare GET /v1/mrb/general-binding-directives/attributes
## Risultato atteso: 200 OK con response body GeneralBindingDirectiveAttributesDto

## Descrizione: Si ottengono gli attributi generali vincolanti della direttiva

import utils, constants, json, general, general_response_schemas

expected_status_code = constants.OK_200

def TC0007_GET_Attributes():
  
  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = general.GET_attributes()
  
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
    
      schema = general_response_schemas.GeneralBindingDirectiveAttributesDto
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso GeneralBindingDirectiveAttributesDto')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))
        
        ## Mi salvo tutto il body che mi servirà per test successivi
        Project.Variables.ResponseBody_General_attributes = json.dumps(response_body_dict, default=str)