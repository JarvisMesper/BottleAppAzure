import requests 
import os
import sys

class QuerryError(Exception):
        
        BAD_REQUEST = 0x01
        BAD_KEY = 0x02
        NO_MATCHING = 0x03
        NO_NAME = 0x04

        def __init__(self, id_error, message):
            self.id_error = id_error
            self.message = message
            
class RequestOpenFood:

    BASE_URL='https://www.openfood.ch/api/v2'
    OPENFOOD_API_KEY=os.environ.get('OPENFOOD_API_KEY')
    URL_SEARCH = BASE_URL + '/products/_search'
    URL_NUTRIENT = BASE_URL + '/nutrients'
    QUERY_SUCCEED = 200
    
