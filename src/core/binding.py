from google.appengine.ext import db
#from models import DomainTable
from models import Domain 
import functions
from core import compute_next


def bind(domain,mydomain):
    ''' 
    
    '''    
    last_assignment = ''
    
    #dt=DomainTable()
    domain = Domain()
    #query = db.Query(DomainTable).filter('domain = ',domain)
    query = db.Query(Domain).filter('name = ', domain)
    if query.count() != 0:
        dt = query.fetch(1)[0]
        last_assignment = dt.last_assignament
        
    while True:
        last_assignment = compute_next(last_assignment)
        short = '/'.join( (mydomain,domain,last_assignment) )
        if not functions.isAlredyCustum(short):
            break
    
    dt.domain = domain
    dt.last_assignament = last_assignment
    db.put(dt)

    return dt.last_assignament
