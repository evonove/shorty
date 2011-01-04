from google.appengine.ext import db
#from models import DomainTable
from models import Domain 
import functions
from core import compute_next


def bind(domain_s,mydomain):
    ''' 
    
    '''    
    last_assignament = ''
    
    #dt=DomainTable()
    #domain = Domain()
    #query = db.Query(DomainTable).filter('domain = ',domain)
    query = db.Query(Domain).filter('name_domain = ', domain_s)
    if query.count() != 0:
        dt = query.fetch(1)[0]
        last_assignament = dt.last_assignament
        
    while True:
        last_assignament = compute_next(last_assignament)
        short = '/'.join( (mydomain,domain_s,last_assignament) )
        if not functions.isAlredyCustum(short):
            break
    
    #dt.domain = domain_s
    dt.last_assignament = last_assignament
    db.put(dt)

    return dt.last_assignament
