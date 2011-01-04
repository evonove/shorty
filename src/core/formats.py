from StringIO import StringIO
from django.utils import simplejson as json
import time


class Response():
    """
    This class provide the instrument to codify teh Response
    
    Fields
    
        message - the replay : list of string 
        date - the date of the request : string
        error - message of error : string
        error_code - the code of error : string
        total_short - number of shorted url : integer
        type - type of replay, the default is json : string    
    
    
    """
    def __init__(self,message,initial_date,error,error_code,total_short):
        #message e' una lista ricordare di passarla come tale 
        self.message=message
        self.date = str(initial_date)
        self.error = error
        self.error_code = error_code
        self.total_short=total_short 
        
            

    def serializeJson(self):
        '''
        create a json object
    
        Params
    
        Return
            response : json 
        '''
        response =  json.dumps({"Header":({"Date":self.date,\
        "Total_short":self.total_short,"Error":self.error,\
        "Error_id":self.error_code}), "Body":{"Message":self.message}})
        return response

    def makeXml(self):
        pass



class DecodeJson():
    """
    
    """
    def __init__(self,response):
        self.json_object = json.load( StringIO(response))  
    
    def getMessage(self):
        return  self.json_object["Body"]["Message"]
    
    def getDate(self):
        return  self.json_object["Header"]["Date"]
    
    def isError(self):
        return  self.json_object["Header"]["Error"]
    
    def getErrorCode(self):
        return  self.json_object["Header"]["Error_id"] 
    
    def totalShort(self):
        return  self.json_object["Header"]["Total_short"]
    
