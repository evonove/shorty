from google.appengine.ext import db
from models import DomainTable
import string

def bind(domain):
    ''' 
    
    '''
    letters = [x for x in string.ascii_letters]
    numbers = [str(x) for x in xrange(10)]
    grammar = letters + numbers
    separator = ["_","-","+"]
    
    dt=DomainTable()
    query = db.Query(DomainTable).filter('domain = ',domain)
    if query.count()==0:
        dt.domain = domain
        dt.last_assignament = "_AA"
        db.put(dt)
        return dt.last_assignament 
    else:
        dt = query.fetch(1)[0]
        short = computeShortTag(grammar,separator,dt.last_assignament)
        dt.last_assignament=short
        db.put(dt)
        return dt.last_assignament
    
                
def computeShortTag (grammar,separator,last):
    '''

    '''

    index_sep = separator.index(last[0])
    index_frist = grammar.index(last[1])
    index_sec=grammar.index(last[2])
    index_sec = index_sec + 1
    if index_sec%61==0:
        index_sec=0
        index_frist=index_frist+1
        if index_frist%61==0:
            index_frist=0
            index_sep=index_sep+1
    tag = separator[index_sep]+grammar[index_frist]+grammar[index_sec]
    return tag
    
  
def control(domain):
    '''
    
    '''
    dt2 = DomainTable()
    query = db.Query(DomainTable).filter('domain = ',domain)
    dt2 = query.fetch(1)[0]
    print dt2.domain
    print dt2.last_assignament
    
'''    
def main():
    bind("power_ranger")
    control("power_ranger")

     
  
if __name__ == "__main__":
    main()
'''   
    
    