############################################################ RESPONSE CODES ############################################################
OK_200 = 200
CREATED_201 = 201
NO_CONTENT_204 = 204
BAD_REQUEST_400 = 400
FORBIDDEN_403_401 = [403, 401]
NOT_FOUND_404 = 404
ERROR_500 = 500
CONFLICT_409 = 409
UNAUTHORIZED_401 = 401
FORBIDDEN_403 = 403

RESPONSE_STATUS_ERRATO = 'Response status NON CORRETTO, lo status code PREVISTO era: '
RESPONSE_STATUS_CORRETTO = 'Response status CORRETTO'

############################################################ TC LOGS ############################################################
RESP_NESSUN_ITEM_OK = 'Il servizio non ha restituito alcun item'
RESP_NESSUN_ITEM_KO = 'NON è STATO RESTITUITO ALCUN ITEM, il body o il campo content risultano vuoti'
RESP_ITEM_PRESENTI_KO = 'Il servizio ha restituito degli item: verificare di aver cercato un item non esistente'
RESP_NO_CAMPO_CONTENT_KO = 'LA RESPONSE CONTIENE UN BODY ERRATO, il campo content non esiste'
RESP_NO_BODY = 'La response non contiene un body'