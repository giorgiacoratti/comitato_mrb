import generic_calls, json

base_url = ProjectSuite.Variables.base_path
token = ProjectSuite.Variables.token_8883
  
  
  
""" 
  Metodo che crea una GET request e la invia all'endpoint al path 
  /v1/mrb/evaluation-areas-config/areas
"""
def GET_areas() :
  path = '/v1/mrb/evaluation-areas-config/areas'
  url = base_url+path
  return generic_calls.send_request_generic('GET', url, token, path)