## Descrizione: Lanciare GET /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/areas/{areaId}
## Risultato atteso: 200 OK con response body EvaluationAreaDetailDto

## Prerequisito: TC0001 ( report_id ), TC0011 ( quarterly_detail_id ) e TC0017 ( area_id )
## Salvo la variabile elemet_id
## Descrizione: Si ottengono i dettagli trimestrali dell'area relativa all'id area_id

import utils, constants, json, evaluation_areas, evaluation_areas_response_schemas

expected_status_code = constants.OK_200

def TC0018_GET_AreaId():
  
  ## Estraggo il body dal file .json e lo converto in obj per verificarne il formato 
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
    
  ## Salvo la variabile areaId
  if Project.Variables.area_id :
    area_id = Project.Variables.area_id
  else:
    Log.Error('areaId non presente nelle Project Variables! Lanciare l\'Execution Group o valorizzare la Project Variable')
  
  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  resp = evaluation_areas.GET_area_id(report_id, quarterly_detail_id, area_id)
  
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
    
      schema = evaluation_areas_response_schemas.EvaluationAreaDetailDto
    
      if not utils.validate(schema, response_body_dict):
        Log.Warning('La risposta del servizio NON rispetta lo schema atteso, verificare')
        Log.Warning('Response body: '+json.dumps(response_body_dict, default=str, indent=4))
        Log.Warning('Schema atteso: '+json.dumps(schema, default=str, indent=4))
        
      else:
        
        Log.Message('La response del servizio rispetta lo schema atteso EvaluationAreaDetailDto')        
        Log.Message('Item restituito: '+json.dumps(response_body_dict, default=str, indent=4))
        
        if not response_body_dict['elements'][1]['id'] and not response_body_dict['elements'][1]['currentQuarterFields'][0]['id'] and not response_body_dict['elements'][1]['currentQuarterFields'][0]['type'] :
          Log.Error('Non è stato restituito nessun elemento, verificare!')
        else:
          Project.Variables.element_id = response_body_dict['elements'][1]['id']
          Project.Variables.element_quarter_fields_id = response_body_dict['elements'][1]['currentQuarterFields'][0]['id']
          Project.Variables.element_quarter_fields_type = response_body_dict['elements'][1]['currentQuarterFields'][0]['type']
          Log.Message('E\' stato salvato l\'elemento con id: '+str(Project.Variables.element_id)+'. Il valore dell\'id e del type di currentQuarterFields sono rispettivamente: '+str(Project.Variables.element_quarter_fields_id)+' e '+str(Project.Variables.element_quarter_fields_type))