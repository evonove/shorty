from StringIO import StringIO
from django.utils import simplejson as json
import time


class CodeJson():
    """
    
    """
    def __init__(self,message,initial_date,error,error_code,total_short):
        #message e' una lista ricordare di passarla come tale 
        self.message=message
        self.start_time = initial_date
        self.error = error
        self.error_code = error_code
        self.total_short=total_short
        self.stop_date = time.mktime(time.localtime())

    def serializeJson(self):
        '''

        '''
        response =  json.dumps({"Header":({"Start_date":self.start_time,\
        "Stop_date":self.stop_date,"Total_short":self.total_short,"Error":self.error,\
        "Error_id":self.error_code}), "Body":{"Message":self.message}})
        return response


class DecodeJson():
    """
    
    """
    def __init__(self,response):
        self.json_object = json.load( StringIO(response))  
    
    def getMessage(self):
        return  self.json_object["Body"]["Message"]
    
    def getStartDate(self):
        return  self.json_object["Header"]["Start_date"]
    
    def isError(self):
        return  self.json_object["Header"]["Error"]
    
    def getErrorCode(self):
        return  self.json_object["Header"]["Error_id"] 
    
    def totalShort(self):
        return  self.json_object["Header"]["Total_short"]
    
    def getStopDate(self):
        return  self.json_object["Header"]["Stop_date"]
