from google.appengine.ext import db
from binding import bind
from models import UrlBox
from urlparse import urlparse
import formats
import whitelist
import time
import sys 

def core_classic(url):
    '''
    '''
    try :
        if isShorted(url):
            du=UrlBox()
            query = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True)
            du = query.fetch(1)[0]
            #shorted = du.shorted_url
            message_list=[]
            message_list.append(du.shorted_url)
            resp = formats.CodeJson(message_list,du.date,False,"0",totals())
            json_object = resp.serializeJson()
            return json_object
         
        else:
            mydomain="www.cerbero.it"
            dominio = computeDomain(url)
            is_recycle=isReciclable(dominio)
            if is_recycle:
                shorted = recycle(dominio,url)
                message_list=[]
                message_list.append(shorted[0])
                resp = formats.CodeJson(message_list,shorted[1],False,"0",totals())
                json_object = resp.serializeJson()
                return json_object
            else:
                shorted = bind(dominio,mydomain) 
                url_shortato = mydomain+dominio+shorted
                dt=UrlBox()
                dt.domain = dominio
                dt.url = url 
                dt.shorted_url=url_shortato
                dt.date=time.mktime(time.localtime())
                dt.active = True
                db.put(dt)
                message_list=[]
                message_list.append(dt.shorted_url)  
                resp = formats.CodeJson(message_list,dt.date,False,"0",totals())
                json_object = resp.serializeJson()
                return json_object
    except:
        error = str(sys.exc_info()[0])
        date=time.mktime(time.localtime())
        message_list=["si e' verificato un errore : "+str(error)] 
        resp = formats.CodeJson(message_list,date,True,"1",totals())
        json_object = resp.serializeJson()
        return json_object  

    
def core_custum(url,user_url):
    '''
    '''
    try : 
        mydomain="www.cerbero.it/"
        dominio = computeDomain(url)
        url_shortato = mydomain+dominio+"_"+user_url    
        if isAlredyCustum(url_shortato):
            date=time.mktime(time.localtime())
            message_list=["si e' verificato un errore : "+ "url gia' assegnato"]
            resp = formats.CodeJson(message_list,date,True,"1",totals())
            json_object = resp.serializeJson()
            return json_object
            
        else:
            dt=UrlBox()
            if isReciclableCustum(url_shortato):
                query = db.Query(UrlBox).filter('shorted_url = ', url_shortato ).filter('active = ' , False)
                dt = query.fetch(1)[0]
                dt.shorted_url = url_shortato 
                dt.date=time.mktime(time.localtime())
                dt.active = True
                db.put(dt)     
                message_list=[dt.shorted_url]
                resp = formats.CodeJson(message_list,dt.date,False,"0",totals())
                json_object = resp.serializeJson()
                return json_object
            else:
                dt.domain = dominio
                dt.url = url 
                dt.shorted_url=url_shortato
                dt.date=time.mktime(time.localtime())
                dt.active = True
                db.put(dt)
                message_list=[dt.shorted_url]
                resp = formats.CodeJson(message_list,dt.date,False,"0",totals())
                json_object = resp.serializeJson()
                return json_object
                
    except:
        error = str(sys.exc_info()[0])
        date=time.mktime(time.localtime())
        message_list=["si e' verificato un errore : "+str(error)]
        resp = formats.CodeJson(message_list,date,True,"0",totals())
        json_object = resp.serializeJson()
        return json_object


def get_shorts(domain, limit, offset=0):
    '''Retrieve shorted urls for a certain domain.
    
    Params
        domain - the domain for which retrieve results: string
        limit - how many results at max to retrieve: int
        offset - how many results to skip: int
    
    Return
        a list containing shorted urls for the domain: list
    '''
    query = db.Query(UrlBox).filter('domain = ', domain)
    results = query.fetch(limit, offset)
    return [x.shorted_url for x in results]


def num_of_shorts(domain=None):
    '''Count how many shorts we've got in the datastore
    
    Params
        domain - if not None count shorts for that domain, count all otherwise
    
    Return
        number of shorts: integer
    '''
    query = UrlBox.all()
    if domain:
        query.filter(' domain = ', domain)
    return query.count()


def is_short(shorted_url):
    '''Check if a shorted url is known to the system, and in case if it is
    currently active
    
    Params
        shorted_url - an already shorted url to check: string
        
    Return
        whether shorted url is known and active: boolean
    '''
    query = db.Query(UrlBox, keys_only=True)
    query.filter('shorted_url = ', shorted_url).filter('active = ' , True)
    return query.count() > 0


def already_shorted(url):
    '''Check if an url was already shorted
    
    Params
        url - url to check: string
    
    Return
        whether the url was already shorted: boolean
    '''
    query = db.Query(UrlBox, keys_only=True)
    query.filter('url = ', url).filter('active = ', True)
    return query.count() > 0


def isReciclableCustum(shorted_url):
    '''
    '''
    query = db.Query(UrlBox).filter('shorted_url = ',shorted_url).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
        

def isReciclable(dominio):
    '''
    '''
    #dt=UrlBox()
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
    

def recycle(dominio,url):
    '''
    '''
    dt=UrlBox()
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    dt = query.fetch(1)[0]
    dt.active=True
    dt.url = url
    dt.date = time.mktime(time.localtime())
    shorted = dt.shorted_url
    db.put(dt)
    info=[]
    info[0]=shorted
    info[1]= dt.date
    return info
    
def getRealUrl(shorted_url):
    du=UrlBox()
    query = db.Query(UrlBox).filter('shorted_url = ',shorted_url )
    du = query.fetch(1)[0]
    du.last_click=time.mktime(time.localtime())
    db.put(du) 
    return du.url

def cancelPolicy(soglia):
    data_from_cancel = time.mktime(time.localtime()) - soglia
    query = db.Query(UrlBox).filter('last_click < ', data_from_cancel)
    results = query.all
    for res in results:
        db.delete(res)
    

def computeDomain(url):
    '''
    '''
    if url[0:7]!="http://":
        url ="http://"+url
    parsed = urlparse(url)
    domain = parsed.hostname
    if domain[0:4]=="www.":
            domain = domain[4:len(domain)]
    
    if whitelist.checkInWhite(domain):
        domain = domain[0:len(domain)-3]
    
    return domain


def cancel(url_short):
    try:
        dt=UrlBox()
        query = db.Query(UrlBox).filter('shorted_url = ',url_short ).filter('active = ', True)
        if query.count()>0:
            dt = query.fetch(1)[0]
            dt.active=False
            db.put(dt)
        else:
            print "attenzione"
            print "errore url non presente"
    except:
        error = str(sys.exc_info()[0])
        print error

