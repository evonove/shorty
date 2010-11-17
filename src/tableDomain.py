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

    def WriteAssociation(self,domain):
        #attenzione se ho già il dominio devo solo aggiornare
        
        self.domain = domain
        index=self.ReadAssociation(domain)
        if (index[0]==0 and index[1]== 0 and index[2]==1):
            self.counterSeparator = index[0]
            self.counterFrist = index[1]
            self.counterSecond = index[2]
            self.put()
        else:
            index=self.IncrementalIndex(index)
            self.UpdateDomain(domain,index)
        #self.counterSeparator = separator
        #self.counterFrist = frist
        #self.counterSecond = second
          
        
    
      
    def UpdateDomain(self,domain,index):
        q = db.GqlQuery("UPDATE DomainTable set counterSeparator:=1,counterFrist:=2,counterSecond:=3"+ 
                        "WHERE domain=:4 ",index[0],index[1],index[2],domain)
        
    def CancelAssociation(self,domain):
        indici=[]     
        index=self.ReadAssociation(domain)
        index=self.DecrementalIndex(index)
        self.UpdateDomain(domain,index)
        
    def ReadAssociation(self,dominio):
        
        #se e' la prima occorre una strating hand
        #q2=db.GqlQuery("SELECT COUNT FROM DomainTable WHERE domain=:1",dominio)
        #res = q2.fetch(10)
        #for i in res :
        #    print i
        
        
        q = db.GqlQuery("SELECT * FROM DomainTable WHERE domain=:1 ORDER BY counterSeparator,counterFrist,counterSecond ",dominio)
        
        indici=[]
        results = q.fetch(10)
        
        if len(results)==0:
            indici.insert(0,0)
            indici.insert(1,1)
            indici.insert(2,2)
        else:
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
    domain_table.WriteAssociation("libero")
    #domain_table.WriteAssociation("aaaaa",1,1,2)
    #domain_table.WriteAssociation("ccccc",1,1,3)
    #indici=[]
    #indici=domain_table.ReadAssociation("ccccc")
    #indici = domain_table.IncrementalIndex(indici)
    
    #print "via"
    #for i in range (0,3):
    #    print "nuovo indice :" + str(indici[i])
    
       
    
if __name__ == "__main__":
    main()
 
    
    
    
        