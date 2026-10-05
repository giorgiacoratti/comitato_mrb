import sys
sys.path.insert(0, "../lib")
import json, string, random
from datetime import datetime, timedelta, time #, date, calendar
from operator import itemgetter
from urllib.parse import urlencode
#from schema import Schema, And, Use, Optional, SchemaError

############################################################ Funzioni di date retrieval ############################################################

"""
  Restituisce una stringa datetime, con formato mappato
  @param days_delta:int OPZ -> default 0, nessun delta > per giorni futuri passo un valore positivo, per giorni passati un valore negativo
  @param format:str OPZ -> default '%d%m%y'
  
"""
def get_date_custom_format(days_delta=0, format="%d%m%y"):
  dt = datetime.now() + timedelta(days=days_delta)
  return dt.strftime(format)
  
"""
  Converte un datitime in una stringa
  @param dt: oggetto datetime da convertire
  @param format - opzionale: stringa contentente la formattazione della stringa datetime, es. '%d/%m/%Y' (esempio: 08/03/2024)
                             se non valorizzato, la stringa datetime avrà formato '%Y-%m-%dT%H:%M:%SZ'
  @returns str or None
"""
def convert_datetime_to_str(dt, format='%Y-%m-%dT%H:%M:%SZ'):
  if isinstance(dt, datetime):
    return dt.strftime(format)
  else:
    return None  

"""
  Modifica una data stringhifizzata aggiungendo o sottraendo giorni
"""
def change_date_by_days(date_str, days_to_add=None, days_to_subtract=None, input_format='%Y-%m-%dT%H:%M:%SZ', output_format='%Y-%m-%dT%H:%M:%SZ'):
  if days_to_add != None:
    try:
      dt = datetime.strptime(date_str, input_format) + timedelta(days=days_to_add)
      return dt.strftime(output_format)
    except TypeError:
      dt = datetime(*(time.strptime(date_str, input_format)[0:6])) + timedelta(days=days_to_add)
      return dt.strftime(output_format)
      
  if days_to_subtract != None:
    try:
      dt = datetime.strptime(date_str, input_format) + timedelta(days=-abs(days_to_subtract))
      return dt.strftime(output_format)
    except:
      dt = datetime(*(time.strptime(date_str, input_format)[0:6])) + timedelta(days=-abs(days_to_subtract))
      return dt.strftime(output_format)    
      
"""
  Modifica il formato di una data, e aggiunge o sottrae giorni > versione migliorata di change_date_by_days
  @param input_date_string data stringhifizzata
  @param input_format:OPZ -> default '%d%m%y', formato della input_date_string
  @param output_format:str OPZ -> default '%d-%m-%Y', formato desiderato in output
    
"""
def convert_date_format(input_date_string, input_format="%d%m%y", output_format="%d/%m/%Y", days_delta=0):  
  try:
    dt = datetime.strptime(input_date_string, input_format) + timedelta(days=days_delta)
  except TypeError:
    dt = datetime(*(time.strptime(input_date_string, input_format)[0:6])) + timedelta(days=days_delta)
  
  return dt.strftime(output_format)
    
#"""
#  Modifica il mese della data passata: default restituisce il mese precedente
#  @param orig_date
#  @param months: delta di mesi da aggiungere a orig_date -> es months -3 tre mesi prima, months 3 tre mesi dopo rispetto a orig_date
#"""
#def change_date_by_month(orig_date, months=-1):
#    new_year = orig_date.year
#    new_month = orig_date.month + months
#    if new_month > 12:
#        new_year += 1
#        new_month -= 12
#    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
#    new_day = min(orig_date.day, last_day_of_month)
#
#    return orig_date.replace(year=new_year, month=new_month, day=new_day)
  
"""
  Restituisce la data più alta in un array di datetime stringhifizzate
  @param datetime_str_array
  @param input_format
  @param output_format
  @param delta_from_today -> default False, se passato a True restituisco anche il delta tra la data massima dell'array e la data odierna
  @return la data massima dell'array, e se delta_from_today=True, il delta tra la data massima e la data odierna
"""  
def get_max_date(datetime_str_array, input_format="%Y-%m-%dT%H:%M:%S", output_format="%Y-%m-%dT%H:%M:%S", delta_from_today=False):
  
  datetime_array = []
  for item in datetime_str_array:
    try:
      datetime_array.append(datetime.strptime(item, input_format))
    except TypeError:
      datetime_array.append(datetime(*(time.strptime(item, input_format)[0:6])))
      
    latest = max(datetime_array)  
    if delta_from_today == True:
      dt_delta = latest.date() - datetime.now().date()
      return latest.strftime(output_format), dt_delta.days
    else:
      return latest.strftime(output_format)
    
######################################################### Funzioni di creazione stringhe ##############################################################

def generate_random_string(lenght=50):
  return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(lenght))
  
def generate_random_number(lenght=10):
  return int(''.join(random.choice(string.digits) for i in range(lenght)))
  
"""
  Restituisce una stringa composta da base+number_lenght di cifre, per default FKT+4 > esempio FKT0000
  @param opz base
  @param opz number lenght
"""
def generate_random_char_digit_string(base_length=3, numbers_lenght=5):
  random_letter = (random.choice(string.ascii_letters) for i in range(base_length))
  base = ''.join(random_letter)
  numbers = (random.choice(string.digits) for i in range(numbers_lenght))
  output = ''.join(numbers)
  return base.upper() + output

############################################################ Funzioni di mappatura oggetti ############################################################

"""
  Legge file json al path passato e restituisce l'oggetto JSON.
  @param file_path: string
  @returns JSON_obj: dict
"""
def JSON_file_to_obj(file_path):
  try:
    if not aqFile.Exists(file_path):
      Log.Error('JSON file path errato')
      
    JSON_file_content = aqFile.ReadWholeTextFile(file_path, aqFile.ctUTF8)
    JSON_obj = json.loads(JSON_file_content.rstrip())
    
    if JSON_obj == None:
      Log.Error('JSON object non trovato')
      
    return JSON_obj
    
  except Exception as e:
    Log.Error('Errore in JSON_file_to_obj '+str(e))

"""
  Converte il JSON in una query string.
  @param query_param_obj: JSON (non annidato) dei query parameters
  @return query_string: stringa nel formato query string
"""
def obj_to_query_string(query_param_obj):
  try:
#    key_value_pairs = []
#
#    # Itero sugli item del dizionario e aggiungo all'array le coppie encoded
#    for key, value in query_param_obj.items():
#        key_value_pairs.append(f"{key}={value}")
#  
#    # Unisco gli elementi della lista in una stringa separandoli con la "&"
#    query_string = "&".join(key_value_pairs)
#    
#    if ':' in query_string: 
#      replace(':', '%3A')
  
    query_string = urlencode(query_param_obj)
    return query_string;
    
  except Exception as e:
    Log.Error('Errore in obj_to_query_string: '+str(e))
  
"""
  Cicla l'oggetto content e restituisce l'array di id degli items che contiene e l'array di bodies degli items'
  @param content: array di dict (assets)
  returns item_id_arr array di int (gli id degli item presenti in content)
          item_body_arr array di items
  
"""
def get_content_items_ids_and_bodies(content):
  # array di contractId 
  item_id_arr = []
  item_body_arr = []
      
  # ciclo gli item presenti in content
  for item in content:
    item_id_arr.append(int(item['id']))
    
    # Parso l'id ad intero (per consentire ordinamenti)
    item['id'] = int(item.get('id'))
    item_body_arr.append(item)
  
  return item_id_arr, item_body_arr
  
"""
  Restituisce un array di json a partire da un csv, ove le chiavi del json saranno le colonne del csv
  @param csv_string:string
  @returns lines_obj_arr:dict[]
"""
def map_csv_to_json(csv_string):
  lines_arr = csv_string.split("\n")
  columns_arr = lines_arr[0].split(';')
  lines_arr.pop(0)
  
  lines_obj_arr = []
  
  if columns_arr != [] and lines_arr != []:
    for line_str in lines_arr:
      line_values_arr = line_str.split(';')
      line_obj = {}
      for i, column in enumerate(columns_arr):
        line_obj.update({ column : line_values_arr[i] })
    
      lines_obj_arr.append(line_obj)
    
  return lines_obj_arr
  
############################################################ Funzioni di comparazione ############################################################

def validate(schema, data):
#  return schema.is_valid(data)
  try:
    return schema.validate(data)
  except Exception as e:
    Log.Message('Errore nella validazione dei dati: '+str(e))

"""
  Confronta due oggetti, request che ha creato l'item e response della ricerca per id dell'item, e logga gli errori
  @param main_JSON: oggetto da verificare, se i suoi campi non nulli o vuoti esistono nel comparison JSON, il valore deve corrispondere
  @param comparison_JSON: oggetto contro cui verificare main_JSON
"""
def compare_objects_request_resp(main_JSON, comparison_JSON):
  corresponding_fields = {}
  for main_JSON_key in main_JSON.keys():
    
    # Se il campo corrente del JSON principale non è null o vuoto
    if main_JSON.get(main_JSON_key) != None and main_JSON.get(main_JSON_key) != '':
      # se la chiave corrente del JSON principale esiste nel JSON di comparazione
      if main_JSON_key in comparison_JSON: 
     
        # Gestisco la comparazione tra date come stringhe (ASSUMENDO che siano stringhe con formato "YYYY-mm-dd'T'HH:MM:SS" o "YYYY-mm-dd'T'HH:MM:SSZ")
        if isinstance(main_JSON.get(main_JSON_key), str) and '-' in main_JSON.get(main_JSON_key) and 'T' in main_JSON.get(main_JSON_key) and ':' in main_JSON.get(main_JSON_key):
          main_JSON_date_string = main_JSON.get(main_JSON_key)[0:10]
          comparison_JSON_date_string = comparison_JSON.get(main_JSON_key)[0:10]
          if main_JSON_date_string != comparison_JSON_date_string:
            Log.Warning( 'Il valore del campo '+main_JSON_key+' non coincide: nella request era '+str(main_JSON.get(main_JSON_key))+', mentre nella response è: '+str(comparison_JSON.get(main_JSON_key)) )
          else:
            corresponding_fields.update({ main_JSON_key : str(main_JSON.get(main_JSON_key)) })
        
        # Non gestisco la comparazione di chiavi che contengono array > valutare se da aggiungere    
        elif str(main_JSON.get(main_JSON_key)) != str(comparison_JSON.get(main_JSON_key)) and not isinstance(main_JSON.get(main_JSON_key), list):
          Log.Warning( 'Il valore del campo '+main_JSON_key+' non coincide: nella request era '+str(main_JSON.get(main_JSON_key))+', mentre nella response è: '+str(comparison_JSON.get(main_JSON_key)) )
          #return {}
        else:
          corresponding_fields.update({ main_JSON_key : str(main_JSON.get(main_JSON_key)) })
          
  return corresponding_fields
          
"""
  Confronta due array di oggetti, response del servizio e query output, e logga i risultati > ASSUMENDO che i due oggetti abbiano chiavi con gli stessi nomi!
  @param resp_JSON_arr: array di oggetti (campo 'content' o simili del response body, contenente un array di oggetti)
  @param query_output_JSON_arr: array di oggetti (record restituiti dalla query e mappati come un array di oggetti - ciascun record un oggetto)
  @param already_ordered:opz, quando in default (False), gli oggetti all'interno dei due array vengono ordinati per il valore dell'id  
"""
def compare_array_body_records(resp_JSON_arr, query_output_JSON_arr, already_ordered=False):
  
  same_fields_obj_arr = []
  
  # Ordino le due liste di dict per il valore del campo id
  if already_ordered == False:
    #resp_JSON_arr, query_output_JSON_arr = [sorted(i, key=itemgetter("id")) for i in (resp_JSON_arr, query_output_JSON_arr)]
    resp_JSON_arr = sorted(resp_JSON_arr, key=lambda d: d['id'])
    query_output_JSON_arr = sorted(query_output_JSON_arr, key=lambda d: d['id'])
  
  # Itero lo zip delle due liste di dict
  for resp_item_JSON, single_record_JSON in zip(resp_JSON_arr, query_output_JSON_arr):
  
      same_fields_obj = {}
      
      # Itero le chiavi del record corrente (cioè le colonne)
      for record_key in single_record_JSON.keys():
        if single_record_JSON.get(record_key) != None and single_record_JSON.get(record_key) != '':
        
          # Converto la chiave dallo snake_case del record al camelCase dell'oggetto della response
          record_key_camel = snake_to_camel(record_key)
          
          ## Se la chiave corrente del record corrente è presente nel dict corrente della response ##
          if record_key_camel in resp_item_JSON:
          
            # Gestisco la comparazione tra date come stringhe (ASSUMENDO che in resp_item_JSON siano stringa con formato "YYYY-mm-dd'T'HH:MM:SS") #
            if isinstance(single_record_JSON.get(record_key), datetime):
              record_date_string = single_record_JSON.get(record_key).strftime("%Y-%m-%d")
              resp_date_string = resp_item_JSON.get(record_key_camel)[0:10]
              
              if resp_date_string != record_date_string:
                Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
              else:
                same_fields_obj.update({ record_key : str(single_record_JSON.get(record_key)) })
            
            # Gestisco la comparazione di valori booli (in db 0 1)
            elif isinstance(resp_item_JSON.get(record_key_camel), bool):
              
              if resp_item_JSON.get(record_key_camel) == True and single_record_JSON.get(record_key) == 1:
                same_fields_obj.update({ record_key : resp_item_JSON.get(record_key_camel) })
              elif resp_item_JSON.get(record_key_camel) == False and single_record_JSON.get(record_key) == 0:
                same_fields_obj.update({ record_key : resp_item_JSON.get(record_key_camel) })
              else:
                Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
                
            # Gestisco la comparazione di valori float con interi (in db float ad una cifra, nella response interi)
            elif isinstance(single_record_JSON.get(record_key), float):
              if int(single_record_JSON.get(record_key)) != int(resp_item_JSON.get(record_key_camel)):
                Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
              else:
                same_fields_obj.update({ record_key : str(single_record_JSON.get(record_key)) })
              
            # Comparo i valori non datetime, non bool (0-1 db e False True api) e non float (float db e int api) come stringhe per evitare falsi negativi dovuti al type # 
            elif str(resp_item_JSON.get(record_key_camel)) != str(single_record_JSON.get(record_key)):
              Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
            else:
              same_fields_obj.update({ record_key : single_record_JSON.get(record_key)})
              
      if same_fields_obj != {}: same_fields_obj_arr.append(same_fields_obj)        
       
  return same_fields_obj_arr
  
## Aggiung questa funzione (uguale a quella di sopra nella sostanza) per il test TC0050 perché non controllo qualcosa che si chiama id ma che si chiama summaryIndicatorRegistryId
def compare_array_body_records_50(resp_JSON_arr, query_output_JSON_arr, already_ordered=False):
  
  same_fields_obj_arr = []
  
  # Ordino le due liste di dict per il valore del campo id
  if already_ordered == False:
    #resp_JSON_arr, query_output_JSON_arr = [sorted(i, key=itemgetter("id")) for i in (resp_JSON_arr, query_output_JSON_arr)]
    resp_JSON_arr = sorted(resp_JSON_arr, key=lambda d: d['summaryIndicatorRegistryId'])
    query_output_JSON_arr = sorted(query_output_JSON_arr, key=lambda d: d['id'])
  
  # Itero lo zip delle due liste di dict
  for resp_item_JSON, single_record_JSON in zip(resp_JSON_arr, query_output_JSON_arr):
  
      same_fields_obj = {}
      
      # Itero le chiavi del record corrente (cioè le colonne)
      for record_key in single_record_JSON.keys():
        if single_record_JSON.get(record_key) != None and single_record_JSON.get(record_key) != '':
        
          # Converto la chiave dallo snake_case del record al camelCase dell'oggetto della response
          record_key_camel = snake_to_camel(record_key)
          
          ## Se la chiave corrente del record corrente è presente nel dict corrente della response ##
          if record_key_camel in resp_item_JSON:
          
            # Gestisco la comparazione tra date come stringhe (ASSUMENDO che in resp_item_JSON siano stringa con formato "YYYY-mm-dd'T'HH:MM:SS") #
            if isinstance(single_record_JSON.get(record_key), datetime):
              record_date_string = single_record_JSON.get(record_key).strftime("%Y-%m-%d")
              resp_date_string = resp_item_JSON.get(record_key_camel)[0:10]
              
              if resp_date_string != record_date_string:
                Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
              else:
                same_fields_obj.update({ record_key : str(single_record_JSON.get(record_key)) })
            
            # Gestisco la comparazione di valori booli (in db 0 1)
            elif isinstance(resp_item_JSON.get(record_key_camel), bool):
              
              if resp_item_JSON.get(record_key_camel) == True and single_record_JSON.get(record_key) == 1:
                same_fields_obj.update({ record_key : resp_item_JSON.get(record_key_camel) })
              elif resp_item_JSON.get(record_key_camel) == False and single_record_JSON.get(record_key) == 0:
                same_fields_obj.update({ record_key : resp_item_JSON.get(record_key_camel) })
              else:
                Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
                
            # Gestisco la comparazione di valori float con interi (in db float ad una cifra, nella response interi)
            elif isinstance(single_record_JSON.get(record_key), float):
              if int(single_record_JSON.get(record_key)) != int(resp_item_JSON.get(record_key_camel)):
                Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
              else:
                same_fields_obj.update({ record_key : str(single_record_JSON.get(record_key)) })
              
            # Comparo i valori non datetime, non bool (0-1 db e False True api) e non float (float db e int api) come stringhe per evitare falsi negativi dovuti al type # 
            elif str(resp_item_JSON.get(record_key_camel)) != str(single_record_JSON.get(record_key)):
              Log.Warning('Record '+str(single_record_JSON['id'])+': il valore del campo '+record_key+' è '+str(single_record_JSON.get(record_key))+\
                  ' Il servizio ha invece restituito '+str(resp_item_JSON.get(record_key_camel)))
            else:
              same_fields_obj.update({ record_key : single_record_JSON.get(record_key)})
              
      if same_fields_obj != {}: same_fields_obj_arr.append(same_fields_obj)        
       
  return same_fields_obj_arr
  
"""
Confronta due oggetti, request body che ha creato la risorsa e query output, e logga i risultati > ASSUMENDO che i due oggetti abbiano chiavi con gli stessi nomi!
  @param req_body
  @param record_JSON  
"""
def compare_single_body_record(req_body, record_JSON):

      same_fields_obj = {}
      
      # Itero le chiavi del request body
      for body_key in req_body.keys():
        if req_body.get(body_key) != None and req_body.get(body_key) != '':
          body_key_snake = camel_to_snake(body_key)
          
          # Se la chiave corrente del record è presente nel body, verifico che il contenuto coincida
          if body_key_snake in record_JSON:
          
            # Gestisco la comparazione tra date come stringhe (ASSUMENDO che in req_body siano stringa con formato "YYYY-mm-dd'T'HH:MM:SS")
            if isinstance(record_JSON.get(body_key_snake), datetime):
              record_date_string = record_JSON.get(body_key_snake).strftime("%Y-%m-%d")
              req_date_string = req_body.get(body_key)[0:10]
              
              if req_date_string != record_date_string:
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
              else:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              
            # Gestisco la comparazione di valori booli (in db 0 1)
            elif isinstance(req_body.get(body_key), bool):
              
              if req_body.get(body_key) == True and record_JSON.get(body_key_snake) == 1:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              elif req_body.get(body_key) == False and record_JSON.get(body_key_snake) == 0:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              else:
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
                
            # Gestisco la comparazione di valori float con interi (in db float ad una cifra, nella response interi)
            elif isinstance(record_JSON.get(body_key_snake), float):
              if int(record_JSON.get(body_key_snake)) != int(req_body.get(body_key)):
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
              else:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })

            # Comparo i valori non datetime e non bool come stringhe per evitare falsi negativi dovuti al type #  
            elif str(record_JSON.get(body_key_snake)) != str(req_body.get(body_key)):
              Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
            else:
              same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              
      return same_fields_obj      
      
   
## Definisco la stessa funzione per TC0088, passo come argomento della funzione il valore 'id' che devo controllare
#### In questo caso devo prendere dal response body 'legalEntityManagedInvestmentPortfolioConfigId' e non 'id'
def compare_single_body_record_generic_id(req_body, record_JSON, id_field):

      same_fields_obj = {}
      
      # Itero le chiavi del request body
      for body_key in req_body.keys():
        if req_body.get(body_key) != None and req_body.get(body_key) != '':
          body_key_snake = camel_to_snake(body_key)
          
          # Se la chiave corrente del record è presente nel body, verifico che il contenuto coincida
          if body_key_snake in record_JSON:
          
            # Gestisco la comparazione tra date come stringhe (ASSUMENDO che in req_body siano stringa con formato "YYYY-mm-dd'T'HH:MM:SS")
            if isinstance(record_JSON.get(body_key_snake), datetime):
              record_date_string = record_JSON.get(body_key_snake).strftime("%Y-%m-%d")
              req_date_string = req_body.get(body_key)[0:10]
              
              if req_date_string != record_date_string:
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
              else:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              
            # Gestisco la comparazione di valori booli (in db 0 1)
            elif isinstance(req_body.get(body_key), bool):
              
              if req_body.get(body_key) == True and record_JSON.get(body_key_snake) == 1:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              elif req_body.get(body_key) == False and record_JSON.get(body_key_snake) == 0:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              else:
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
                
            # Gestisco la comparazione di valori float con interi (in db float ad una cifra, nella response interi)
            elif isinstance(record_JSON.get(body_key_snake), float):
              if int(record_JSON.get(body_key_snake)) != int(req_body.get(body_key)):
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
              else:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })

            # Comparo i valori non datetime e non bool come stringhe per evitare falsi negativi dovuti al type #  
            elif str(record_JSON.get(body_key_snake)) != str(id_field):
              Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(id_field))
            else:
              same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              
      return same_fields_obj
      
 
## Definisco un'altra funzione compare_single_body_record_float che mi serve per TC0055 in quanto ho un dato float a db
##### Solitamente i dati a db sono int      
def compare_single_body_record_float(req_body, record_JSON):

      same_fields_obj = {}
      
      # Itero le chiavi del request body
      for body_key in req_body.keys():
        if req_body.get(body_key) != None and req_body.get(body_key) != '':
          body_key_snake = camel_to_snake(body_key)
          
          # Se la chiave corrente del record è presente nel body, verifico che il contenuto coincida
          if body_key_snake in record_JSON:
          
            # Gestisco la comparazione tra date come stringhe (ASSUMENDO che in req_body siano stringa con formato "YYYY-mm-dd'T'HH:MM:SS")
            if isinstance(record_JSON.get(body_key_snake), datetime):
              record_date_string = record_JSON.get(body_key_snake).strftime("%Y-%m-%d")
              req_date_string = req_body.get(body_key)[0:10]
              
              if req_date_string != record_date_string:
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
              else:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              
            # Gestisco la comparazione di valori booli (in db 0 1)
            elif isinstance(req_body.get(body_key), bool):
              
              if req_body.get(body_key) == True and record_JSON.get(body_key_snake) == 1:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              elif req_body.get(body_key) == False and record_JSON.get(body_key_snake) == 0:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              else:
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
                
            # Gestisco la comparazione di valori float con interi (in db float ad una cifra, nella response interi)
            elif isinstance(record_JSON.get(body_key_snake), float):
              if float(record_JSON.get(body_key_snake)) != float(req_body.get(body_key)):
                Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
              else:
                same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })

            # Comparo i valori non datetime e non bool come stringhe per evitare falsi negativi dovuti al type #  
            elif str(record_JSON.get(body_key_snake)) != str(req_body.get(body_key)):
              Log.Warning('Record '+str(record_JSON['id'])+': il valore del campo '+str(body_key)+' è '+str(record_JSON.get(body_key_snake))+\
                          ', la request era invece: '+str(req_body.get(body_key)))
            else:
              same_fields_obj.update({ body_key : record_JSON.get(body_key_snake) })
              
      return same_fields_obj

############################## Funzioni di utilità per le funzioni sopra ##############################

""
""
def base_iterate_compare(first_json, second_json):
  
  ## prima: 
  #  - mappare le chiavi perchè siano nello stesso case
  #  - mappare le date in stringhe %Y-%m-%d"
  #  - mappare i float in interi
  #  - mappare gli interi in stringhe
  #  - mappare i booli
  
  same_fields_obj = {}
  for key in first_json.keys():
  
    if first_json.get(key) != None and first_json.get(key) != '':
      # Se la chiave corrente del primo json è presente nel secondo, verifico che il valore coincida
      if key in second_json:
        if first_json.get(key) != second_json.get(key):
          Log.Warning('Il valore del campo '+str(key)+' nel primo json è: '+str(first_json.get(key))+\
                      ', mentre nel secondo: '+str(second_json.get(key)))
        else:
          same_fields_obj.update({ key : second_json.get(key) })
  
  return same_fields_obj
 
"""
  Converte una stringa da snake_case (lowercase) a lower camelCase.
  Usato per convertire le chiavi degli oggetti che mappano i record db (le chiavi vengono .lower() subito durante la mappatura)
  @param input_str stringa da mutare
  @returns stringa in lower camelCase
"""
def snake_to_camel(input_str):
   if '_' in input_str:
    camel_string = "".join(x.capitalize() for x in input_str.lower().split("_"))
    return input_str[0].lower() + camel_string[1:]
   else:
    return input_str

"""
  Converte una stringa da lower camelCase a snake_case.
  Usato per convertire le chiavi degli oggetti restituiti dall response per confrontarle con le chiavi degli oggetti che mappano i record a db (mappate in lowercase)
  @param input_str stringa da mutare
  @returns stringa in lower camelCase
"""
def camel_to_snake(input):
  if any(l.isupper() for l in input):
    snake_string =''.join(['_' + l.lower() if l.isupper() else l for l in input])
    return snake_string
  else:
    return input
    
