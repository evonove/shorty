'''
Created on 12/gen/2011

@author: matteo
'''
from google.appengine.api import memcache
from core.models import User
import hashlib 

class Shield():
    def __init__(self,ip_adress,user=None):
        self.ip_adress=str(ip_adress)
        self.user=user
        if self.user!=None:
            self.ip_adress = self.ip_adress+"-"+hashlib.sha1(self.user.user_name).hexdigest()
        self.shield=False
        self.max_request = 5
        self.setMemCache()
        self.control()
    
    def setMemCache(self):
        if (memcache._CLIENT.add(key = self.ip_adress, value = '0',time=3600))==True:
            self.shield=False 
        else:
            memcache._CLIENT.incr(self.ip_adress)
                
    def control(self):
        information =  memcache._CLIENT.get(self.ip_adress)
        if int(information) > self.max_request:
            self.shield = True
        else:
            self.shield = False   
                
    def getShieldSentence(self):
        return self.shield
    
        
    
            

           

            
        
         
