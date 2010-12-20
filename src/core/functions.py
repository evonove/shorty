from google.appengine.ext import db
from binding import bind
from urlparse import urlparse
import formats
import time
import sys
from models import Domain, UrlBox, WhiteList
from whitelist import checkInWhite


 

def short(url, custom_string=None):
    """
    Perform the shortening of a given url. Optionally use a custom string
    instead of using internal algorithm provided by core module
    
    Params
        url - the url to shorten: url
        custom_string - the string to use to short the link: string
    
    Return
        shorted url: url
    
    """
    if already_shorted(url):
        #return url
        du=UrlBox()
        query = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True)
        du = query.fetch(1)[0]
        message_list=[]
        message_list.append(du.shorted_url)
        resp = formats.CodeJson(message_list,du.date,False,"0",num_of_shorts())
        json_object = resp.serializeJson()
        return json_object
    
    if custom_string:
        #pass
        # TODO core_custom
        try : 
            mydomain="www.cerbero.it/"
            domain_name = computeDomain(url)
            url_shortato = mydomain+domain_name+"/"+custom_string    
            if is_short(url_shortato):
                date=time.mktime(time.localtime())
                message_list=["si e' verificato un errore : "+ "url gia' assegnato"]
                resp = formats.CodeJson(message_list,date,True,"1",num_of_shorts())
                json_object = resp.serializeJson()
                return json_object
            
            else:
                urlbox=UrlBox()
                if isReciclableCustum(url_shortato):
                    query = db.Query(UrlBox).filter('shorted_url = ', url_shortato ).filter('active = ' , False)
                    urlbox = query.fetch(1)[0]
                    urlbox.shorted_url = url_shortato 
                    urlbox.date=time.mktime(time.localtime())
                    urlbox.active = True
                    db.put(urlbox)     
                    message_list=[urlbox.shorted_url]
                    resp = formats.CodeJson(message_list,urlbox.date,False,"0",num_of_shorts())
                    json_object = resp.serializeJson()
                    return json_object
                else:
                    urlbox.domain = forcedGetDomain(domain_name)
                    urlbox.url = url 
                    urlbox.shorted_url=url_shortato
                    urlbox.date=time.mktime(time.localtime())
                    urlbox.active = True
                    db.put(urlbox)
                    message_list=[urlbox.shorted_url]
                    resp = formats.CodeJson(message_list,urlbox.date,False,"0",num_of_shorts())
                    json_object = resp.serializeJson()
                    return json_object
        except:
            error = str(sys.exc_info()[0])
            date=time.mktime(time.localtime())
            message_list=["si e' verificato un errore : "+str(error)]
            resp = formats.CodeJson(message_list,date,True,"0",num_of_shorts())
            json_object = resp.serializeJson()
            return json_object
    else:
        # TODO core_classic
        try :
            mydomain="www.cerbero.it"
            domain_name = computeDomain(url)
            is_recycle=isReciclable(domain_name)
            if is_recycle:
                shorted = recycle(domain_name,url)
                message_list=[]
                message_list.append(shorted[0])
                resp = formats.CodeJson(message_list,shorted[1],False,"0",num_of_shorts())
                json_object = resp.serializeJson()
                return json_object
            else:
                shorted = bind(domain_name,mydomain) 
                url_shortato = mydomain+domain_name+shorted
                urlbox=UrlBox()
                urlbox.domain = domain_name
                urlbox.url = url 
                urlbox.shorted_url=url_shortato
                urlbox.date=time.mktime(time.localtime())
                urlbox.active = True
                db.put(urlbox)
                message_list=[]
                message_list.append(urlbox.shorted_url)  
                resp = formats.CodeJson(message_list,urlbox.date,False,"0",num_of_shorts())
                json_object = resp.serializeJson()
                return json_object
        except:
            error = str(sys.exc_info()[0])
            date=time.mktime(time.localtime())
            message_list=["si e' verificato un errore : "+str(error)] 
            resp = formats.CodeJson(message_list,date,True,"1",num_of_shorts())
            json_object = resp.serializeJson()
            return json_object  
        
def forcedGetDomain(domain_s):
    """
    check in the instance of the specific domain is saved . 
    If yes return a istance of domain, if no save a istance an retrun it 
    
    Params
        domain - the domain to have instace: string
    
    Return
        an istance of domain object : Domain 
    
    """
    query = db.Query(Domain).filter('name_domain = ', domain_s)
    result = query.get()
    domain = Domain()
    if result == None :
        domain.name_domain=domain_s
        db.put(domain)
    else : 
        domain = query.fetch(1)[0] 
    return domain 
    
        
    
"""
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
            resp = formats.CodeJson(message_list,du.date,False,"0",num_of_shorts())
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
                resp = formats.CodeJson(message_list,shorted[1],False,"0",num_of_shorts())
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
                resp = formats.CodeJson(message_list,dt.date,False,"0",num_of_shorts())
                json_object = resp.serializeJson()
                return json_object
    except:
        error = str(sys.exc_info()[0])
        date=time.mktime(time.localtime())
        message_list=["si e' verificato un errore : "+str(error)] 
        resp = formats.CodeJson(message_list,date,True,"1",num_of_shorts())
        json_object = resp.serializeJson()
        return json_object  

"""
"""    
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
            resp = formats.CodeJson(message_list,date,True,"1",num_of_shorts())
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
                resp = formats.CodeJson(message_list,dt.date,False,"0",num_of_shorts())
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
                resp = formats.CodeJson(message_list,dt.date,False,"0",num_of_shorts())
                json_object = resp.serializeJson()
                return json_object
                
    except:
        error = str(sys.exc_info()[0])
        date=time.mktime(time.localtime())
        message_list=["si e' verificato un errore : "+str(error)]
        resp = formats.CodeJson(message_list,date,True,"0",num_of_shorts())
        json_object = resp.serializeJson()
        return json_object

"""
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
    check if a shorted_url produced by core custom is reciclable
    
    Params 
        shorted_url - a shorted url
    
    Return 
        boolean - true if is possible to recicle
    '''
    query = db.Query(UrlBox).filter('shorted_url = ',shorted_url).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
        

def isReciclable(dominio):
    '''
    check if a shorted_url has the active flag to false for recicle
    
    Params 
        dominio - a domain
    
    Return 
        boolean - true if is possible to recicle
    
    '''
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
    
def isAlredyCustum(shorted_url):
    '''
    '''
    query = db.Query(UrlBox).filter('shorted_url = ', shorted_url ).filter('active = ' , True )
    if query.count()>0:
        return True
    
    else :
        return False
    

def recycle(dominio,url):
    '''
    recicle a short url, store it in db 
    
    Params 
        dominio - a valid domain
        url - url to recicle
    
    Return 
        info - a list who contain shorted url and date for response
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
    """
    return the real url associated to a short url 
    
    Params 
        shorted_url - a shorted url
    
    Return 
        url - the real url to redirect
    """
    du=UrlBox()
    query = db.Query(UrlBox).filter('shorted_url = ',shorted_url )
    du = query.fetch(1)[0]
    #du.last_click=time.mktime(time.localtime())
    db.put(du) 
    return du.url

def cancelByPolicy(soglia):
    """
    this is a sample of cancellation policy. In this case, cancel all row in 
    UrlBox table if the the shorted url not used before a certain date 
    
    Params 
        solgia - a date
    
    Return 
        void - cancel rows 
    """
    data_from_cancel = time.mktime(time.localtime()) - soglia
    query = db.Query(UrlBox).filter('last_click < ', data_from_cancel)
    results = query.all
    for res in results:
        db.delete(res)
    

def computeDomain(url):
    """
    extract a domain_s in a valid url 
    
    Params 
        url - a url to extract domain_s
    
    Return 
        string - domain_s  
    """
    
    if url[0:7]!="http://":
        url ="http://"+url
    parsed = urlparse(url)
    domain_s = parsed.hostname
    if domain_s[0:4]=="www.":
        domain_s = domain_s[4:len(domain_s)]
    domain = forcedGetDomain(domain_s)    
    
    #if checkInWhite(domain_s):
        #domain_s = domain_s[0:len(domain_s)-3]    
    if checkInWhite(domain):
        domain_s = domain_s[0:len(domain_s)-3]
    
    return domain_s


def cancel(url_short):
    """
    cancel a short url, mean change the active flag to false 
    
    Params 
        url_short - a shorted_url
    
    Return 
        void - change the flag 
    """
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

