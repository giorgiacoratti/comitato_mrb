## Descrizione: Lanciare GET /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/specific-binding-directives/{id}
## Risultato atteso: 200 OK con response body SpecificBindingDirectiveDto

## Descrizione: Si ottiene una direttiva di associazione specifica

import utils, constants, json, specific, specific_response_schemas

expected_status_code = constants.OK_200

def TC0012_GET_SpecificID():
  
  ## Importo le Project Variables
  Log.Message('--- STEP 0: Importo le Project Variables ---')
  
  ## Salvo la variabile report_id
  if Project.Variables.report_id :
    report_id = Project.Variables.report_id
  else:
    Log.Error('report_id non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
    
  ## Salvo la variabile quarterly_detail_id
  if Project.Variables.quarterly_detail_id :
    quarterly_detail_id = Project.Variables.quarterly_detail_id
  else:
    Log.Error('quarterly_detail_id non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
    
  ## Salvo la variabile specific_binding_id
  if Project.Variables.specific_binding_id :
    specific_binding_id = Project.Variables.specific_binding_id
  else:
    Log.Error('specific_binding_id non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
  
  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = specific.GET_specific(report_id, quarterly_detail_id, specific_binding_id)
  
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
    
      schema = specific_response_schemas.SpecificBindingDirectiveDto
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso SpecificBindingDirectiveDto')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))
        
        ## Mi salvo tutto il body che mi servirà per test successivi
        Project.Variables.ResponseBody_Specific = json.dumps(response_body_dict, default=str)