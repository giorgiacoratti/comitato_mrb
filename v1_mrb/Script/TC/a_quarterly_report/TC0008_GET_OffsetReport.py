## Descrizione: Lanciare GET /v1/mrb/quarterly-reports/{reportId}/offset/{offset}
## Risultato atteso: 200 OK con response body MrbQuarterlyReportDto

## Passo offset = 1 in modo statico perché il parametro offset mi serve solo per dirgli "restituisci 1 item successivo (oppure se offset=2 passami 2 item succesivi"
## Prerequisito: TC0001 ( report_id )
## Descizione: Si ottiene il rapporto trimestrale MRB offset

import utils, constants, json, quarterly_report, quarterly_report_response_schemas

expected_status_code = constants.OK_200

def TC0008_GET_OffsetReport():
  
  ## Estraggo il query parameter dal file .json e lo converto in query string 
  Log.Message('--- STEP 0: Importo le Project Variables ---')
  
  ## Salvo la variabile reportId
  if Project.Variables.report_id :
    report_id = Project.Variables.report_id
  else:
    Log.Error('reportId non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
    
  ## Salvo la variabile offset
  if Project.Variables.offset :
    offset = '0' #Project.Variables.offset
  else:
    Log.Error('offset non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')

  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = quarterly_report.GET_offset_report(report_id, offset)
  
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
    
      schema = quarterly_report_response_schemas.MrbQuarterlyReportDto
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso MrbQuarterlyReportDto')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))