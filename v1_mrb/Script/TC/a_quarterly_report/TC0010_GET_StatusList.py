## Descrizione: Lanciare GET /v1/mrb/quarterly-reports/status
## Risultato atteso: 200 OK con response body ListResultQuarterlyStatus

## Descizione: Si ottiene l'lenco dello stato dei rapporti trimestrali MRB

import utils, constants, json, quarterly_report, quarterly_report_response_schemas

expected_status_code = constants.OK_200

def TC0010_GET_StatusList():

  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = quarterly_report.GET_status_list()
  
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
    
      schema = quarterly_report_response_schemas.ListResultQuarterlyStatus
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso ListResultQuarterlyStatus')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))