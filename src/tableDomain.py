import sys 
import cgi 

from google.appengine.api import users 
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class DomainTable (db.Model):
    domain = db.StringProperty(multiline=False)
    counterSeparator = db.IntegerProperty()
    counterFrist = db.IntegerProperty()
    counterSecond = db.IntegerProperty()

    def WriteAssociation(self,domain,separator,frist,second):
        self.domain = domain
        self.counterSeparator = separator
        self.counterFrist = frist
        self.counterSecond = second
        self.put()  
        
    def ReadAssociation(self,dominio):
        
        q = db.GqlQuery("SELECT * FROM DomainTable WHERE domain=:1 ORDER BY counterSeparator,counterFrist,counterSecond ",dominio)
        results = q.fetch(10)
        indici=[0]
        for result in results:
            indici.insert(0,result.counterSeparator)
            indici.insert(1,result.counterFrist)
            indici.insert(2,result.counterSecond)   
        
        return indici 
    
    def IncrementalIndex(self,index):
        index[2]=index[2]+1
        if index[2]%61==0:
            index[2]=0
            index[1]=index[1]+1
        if index[1]%61==0:
            index[1]=0
            index[0]=index[1]+1
        return index        
        
    def DecrementalIndex(self,index):
        if index[2]==0 and index[1]>0:
            index[1]=index[1]-1
            index[2]=60
        elif index[2]==0 and index[1]==0:
            index[0]=index[0]-1 
            index[1]=60
            index[2]=60
        else:
            index[2]=index[2]-1 
        
        return index   
        
    
def main():
    domain_table=DomainTable()
    #domain_table.WriteAssociation("bbbbb",1,1,1)
    #domain_table.WriteAssociation("aaaaa",1,1,2)
    #domain_table.WriteAssociation("ccccc",1,1,3)
    indici=[]
    indici=domain_table.ReadAssociation("ccccc")
    indici = domain_table.IncrementalIndex(indici)
    
    #print "via"
    #for i in range (0,3):
    #    print "nuovo indice :" + str(indici[i])
    
       
    
if __name__ == "__main__":
    main()
 
    
    
    
        