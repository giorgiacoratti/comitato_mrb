## Descrizione: Lanciare POST /v1/mrb/general-binding-directives/bulk-delete con requesto body un int 
## Risultato atteso: 200 OK

## Descrizione: Vengono eliminate direttive di associazione generali
## Nel body va passato l'id di una direttiva da cancellare

import utils, constants, json, general, general_response_schemas

expected_status_code = constants.OK_200
body_file_path = './TestData/requests/body/W2_TC0004_post_bulk_delete.json'

def TC0004_POST_BulkDelete():
  
  ## Estraggo il body dal file .json e lo converto in obj per verificarne il formato 
  Log.Message('--- STEP 0: Estraggo il body dal file '+body_file_path)
  
  body_obj = utils.JSON_file_to_obj(body_file_path)
  
  if Project.Variables.general_binding_id :
    body_obj = [int(Project.Variables.general_binding_id)]
  else:
    Log.Error('general_binding_id non valorizzata tra le Project Variables, verificare!')
  
  ## Chiamo il servizio
  Log.Message('--- STEP 1: Chiamata al servizio')
  
  Log.Message('Request body: '+json.dumps(body_obj, default=str, indent=4))
  
  resp = general.POST_bulk_delete(body_obj)
  
  ## Verifico e leggo lo status code 
  if resp.StatusCode != expected_status_code:
    if resp.Text != '':
      Log.Warning('Messaggio di errore: '+resp.Text)
    Log.Error('Response status NON CORRETTO. Lo status PREVISTO era: '+str(expected_status_code))
  else:
    Log.Message('Response status CORRETTO.')