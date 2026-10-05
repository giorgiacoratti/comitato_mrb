## Descrizione: Lanciare GET /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}
## Risultato atteso: 200 OK con response body MrbQuarterlyReportToCloseDto

## Prerequisito: TC0001 ( report_id ) e TC0011 ( quarterly_detail_id )
## Descizione: Si ottiene il dettaglio del trimestre

import utils, constants, json, quarterly_details, quarterly_details_response_schemas

expected_status_code = constants.OK_200

def TC0013_GET_Detail():
  
  ## Estraggo il query parameter dal file .json e lo converto in query string 
  Log.Message('--- STEP 0: Importo le Project Variables ---')
  
  ## Salvo la variabile reportId
  if Project.Variables.report_id :
    report_id = Project.Variables.report_id
  else:
    Log.Error('reportId non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
    
  ## Salvo la variabile quarterlyDetailId
  if Project.Variables.quarterly_detail_id :
    quarterly_detail_id = Project.Variables.quarterly_detail_id
  else:
    Log.Error('quarterlyDetailId non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')

  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = quarterly_details.GET_detail(report_id, quarterly_detail_id)
  
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
    
      schema = quarterly_details_response_schemas.QuarterlyDetailDetailDto
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso QuarterlyDetailDetailDto')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))