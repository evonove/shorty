from google.appengine.ext import db
#from models import DomainTable
from models import Domain 
import functions
from core import compute_next


def bind(domain_string, mydomain):
     
    """
    Calculate and save in db the last assignment valid to short classic 
    
    Params
        domain_s - a domain : string
        mydomain - a domain who provide the service : string
    
    Return
        last assignament : string 
    
    """
    last_assignment = ''   

    query = db.Query(Domain).filter('name_domain = ', domain_string)
    if query.count() != 0:
        dt = query.fetch(1)[0]
        last_assignment = dt.last_assignament
        
    while True:
        last_assignament = compute_next(last_assignment)
        short = '/'.join( (mydomain, domain_string, last_assignament) )
        if not functions.isAlredyCustum(short):
            break
    

    dt.last_assignament = last_assignament
    db.put(dt)

    return dt.last_assignament
