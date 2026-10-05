import generic_calls, json

base_url = ProjectSuite.Variables.base_path
token = ProjectSuite.Variables.token_8883
  
  
  
""" 
  Metodo che crea una POST request e la invia all'endpoint al path 
  /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/specific-binding-directives/search
    @param body_obj: body della request in formato JSON
    @param report_id
    @param quarterly_detail_id
"""
def POST_specific_search(body_obj, report_id, quarterly_detail_id) :
  path = '/v1/mrb/quarterly-reports/'+report_id+'/quarterly-details/'+quarterly_detail_id+'/specific-binding-directives/search'
  url = base_url+path
  body_string = json.dumps(body_obj)
  return generic_calls.send_request_generic('POST', url, token, path, body=body_string)
  
  
  
""" 
  Metodo che crea una POST request e la invia all'endpoint al path 
  /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/specific-binding-directives/create
    @param body_obj: body della request in formato JSON
    @param report_id
    @param quarterly_detail_id
"""
def POST_create(body_obj, report_id, quarterly_detail_id) :
  path = '/v1/mrb/quarterly-reports/'+report_id+'/quarterly-details/'+quarterly_detail_id+'/specific-binding-directives/create'
  url = base_url+path
  body_string = json.dumps(body_obj)
  return generic_calls.send_request_generic('POST', url, token, path, body=body_string)
  
  
  
""" 
  Metodo che crea una POST request e la invia all'endpoint al path 
  /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/specific-binding-directives/bulk-delete
    @param body_obj: body della request in formato JSON
    @param report_id
    @param quarterly_detail_id
"""
def POST_bulk_delete(body_obj, report_id, quarterly_detail_id) :
  path = '/v1/mrb/quarterly-reports/'+report_id+'/quarterly-details/'+quarterly_detail_id+'/specific-binding-directives/bulk-delete'
  url = base_url+path
  body_string = json.dumps(body_obj)
  return generic_calls.send_request_generic('POST', url, token, path, body=body_string)
  
  
  
""" 
  Metodo che crea una GET request e la invia all'endpoint al path 
  /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/specific-binding-directives/{id}
    @param report_id
    @param quarterly_detail_id
    @param specific_binding_id
"""
def GET_specific(report_id, quarterly_detail_id, specific_binding_id) :
  path = '/v1/mrb/quarterly-reports/'+report_id+'/quarterly-details/'+quarterly_detail_id+'/specific-binding-directives/'+specific_binding_id
  url = base_url+path
  return generic_calls.send_request_generic('GET', url, token, path)
  
  
  
""" 
  Metodo che crea una PATCH request e la invia all'endpoint al path 
  /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/specific-binding-directives/{id}
    @param body_obj: body della request in formato JSON
    @param report_id
    @param quarterly_detail_id
    @param specific_binding_id
"""
def PATCH_specific(body_obj, report_id, quarterly_detail_id, specific_binding_id) :
  path = '/v1/mrb/quarterly-reports/'+report_id+'/quarterly-details/'+quarterly_detail_id+'/specific-binding-directives/'+specific_binding_id
  url = base_url+path
  body_string = json.dumps(body_obj)
  return generic_calls.send_request_generic('PATCH', url, token, path, body=body_string)