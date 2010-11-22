import simplejson as json
import time


class MakeJson():
        def __init__(self,message,initial_date,error,error_code,total_short):
                #message per me e' una lista 
                self.message=message
                self.start_time = initial_date
                self.error = error
                self.error_code = error_code
                self.total_short=total_short
                self.stop_date = time.mktime(time.localtime())
        def serializeJson(self):
                '''
                '''
                response =  json.dumps({"Header":({"start_date":self.start_time,\
                "stop_date":self.stop_date,"total_short":self.total_short,"Error":self.error,\
                "error_id":self.error_code}), "Body":{"message":self.message}})
                return response
        def printJsonElement(self,item):
            '''
            '''
            if item == "message" :
                for i in self.message:
                    print i
                #print self.message
            elif item == "start_time":
                    print self.start_time
            elif item == "error":
                    print self.error
            elif item == "error_code":
                    print self.error_code
            elif item == "total_short":
                    print self.total_short
            else :
                    print "elemento non trovato"
     
