## Descrizione: Lanciare PATCH /v1/mrb/quarterly-reports/{reportId}/update-dates con request body MrbQuarterlyReportDateDto
## Risultato atteso: 200 OK con response body MrbQuarterlyReportDto

## Prerequisito: TC0001 ( report_id )
## Descrizione: Vengono aggiornate le date del comitato e del consiglio

import utils, constants, json, quarterly_report, quarterly_report_response_schemas

expected_status_code = constants.OK_200
body_file_path = './TestData/requests/body/TC0003_patch_update_dates.json'

def TC0003_PATCH_UpdateDates():
  
  ## Estraggo il body dal file .json e lo converto in obj per verificarne il formato 
  Log.Message('--- STEP 0: Estraggo il body dal file '+body_file_path)
  
  body_obj = utils.JSON_file_to_obj(body_file_path)
  
  ## Salvo la variabile reportId
  if Project.Variables.report_id :
    report_id = Project.Variables.report_id
  else:
    Log.Error('reportId non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
  
  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  Log.Message('Request body: '+json.dumps(body_obj, default=str, indent=4))
  
  resp = quarterly_report.PATCH_update_dates(body_obj, report_id)
  
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