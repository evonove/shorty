from google.appengine.ext import db
from binding import bind
from urlparse import urlparse
import formats
import time
import sys
from models import Domain, UrlBox, WhiteList
from whitelist import checkInWhite
import datetime

 

def short(url,custom_string=None):
    """
    Perform the shortening of a given url. Optionally use a custom string
    instead of using internal algorithm provided by core module
    
    Params
        url - the url to shorten: url
        custom_string - the string to use to short the link: string
    
    Return
        shorted url: url
    
    """
    domain_name = computeDomain(url)
    domain = forcedGetDomain(domain_name)
    mydomain = domain.shorted_name
    
    
    """ 
        this block is valid for the core classic only 
        if already_shorted(url):
            print "alredy"
            urlBox = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True).get()
            message_list=[]
            message_list.append(urlBox.shorted_url)
            json = formats.Response(message_list,urlBox.date,False,"0",num_of_shorts())
            resp = json.serializeJson()
            return resp
    """
  
    
    if custom_string:
        try :         
            url_shortato = mydomain+"/"+domain_name+"/"+custom_string 
            print url_shortato
            if is_short(url_shortato):
                print "is short"
                date=datetime.datetime.now()
                message_list=["si e' verificato un errore : "+ "url gia' assegnato"]
                json = formats.Response(message_list,date,True,"1",num_of_shorts())
                resp = json.serializeJson()
                return resp
            
            else:
                print "is_not_short"
                if isReciclableCustum(url_shortato):    
                    message_list=[url_shortato]
                    json = formats.Response(message_list,datetime.datetime.now,False,"0",num_of_shorts())
                    resp = json.serializeJson()
                    return resp
                else:
                    insertInUrlbox(domain,url,url_shortato)
                    message_list=[url_shortato]
                    json = formats.Response(message_list,datetime.datetime.now,False,"0",num_of_shorts())
                    resp = json.serializeJson()
                    return resp
        except:
            error = str(sys.exc_info()[0])
            date=datetime.datetime.now()
            message_list=["si e' verificato un errore : "+str(error)]
            json = formats.Response(message_list,date,True,"0",num_of_shorts())
            resp = json.serializeJson()
            return resp
    else:
        # TODO core_classic test pass
        try :
            #move this block
            if already_shorted(url):
                urlBox = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True).get()
                message_list=[]
                message_list.append(urlBox.shorted_url)
                json = formats.Response(message_list,urlBox.date,False,"0",num_of_shorts())
                resp = json.serializeJson()
                return resp
            #end move
            is_recycle=isReciclable(domain)
            if is_recycle:
                shorted = recycle(domain,url)
                message_list=[]
                message_list.append(shorted[0])
                json = formats.Response(message_list,shorted[1],False,"0",num_of_shorts())
                resp = json.serializeJson()
                return resp
            else:
                shorted = bind(domain_name,mydomain)
                url_shortato = mydomain+"/"+domain_name+"/"+shorted
                insertInUrlbox(domain,url,url_shortato)
                message_list=[]
                message_list.append(url_shortato)  
                date = datetime.datetime.now()
                json = formats.Response(message_list,date,False,"0",num_of_shorts())
                resp = json.serializeJson()
                return resp
        except:
            error = str(sys.exc_info()[0])
            date=datetime.datetime.now()
            message_list=["si e' verificato un errore : "+str(error)] 
            json = formats.Response(message_list,date,True,"1",num_of_shorts())
            resp = json.serializeJson()
            return resp  
        
        
def insertInUrlbox(domain,url,url_shortato):
    urlbox=UrlBox()
    urlbox.domain = domain
    urlbox.url = url 
    urlbox.shorted_url=url_shortato
    urlbox.date=datetime.datetime.now()
    urlbox.active = True
    urlbox.last_click=datetime.datetime.now()
    db.put(urlbox)
    return True 

        
def forcedGetDomain(domain_s):
    """
    check in the instance of the specific domain is saved . 
    If yes return a istance of domain, if no save a instance an return it 
    
    Params
        domain - the domain to have instace: string
        domain_service - the name of our domain to provide service : strig
                         for the most important sites 
    
    Return
        an istance of domain object : Domain 
    
    """
    query = db.Query(Domain).filter('name_domain = ',domain_s)
    result = query.get()
    domain = Domain()
    if result == None :
        domain.name_domain=domain_s
        db.put(domain)
    else : 
        domain = query.fetch(1)[0] 
    return domain 
    
        
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
        urlbox = query.get()
        urlbox.shorted_url = shorted_url 
        urlbox.date=datetime.datetime.now()
        urlbox.active = True
        db.put(urlbox)     
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
    check if a string is alredy use for shorted_url 
    
    Params 
        shorted_url - a shorted_url : string
    
    Return 
        boolean - true if is used
    
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
    urlbox=UrlBox()
    urlbox = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False).get()
    urlbox.active = True  
    urlbox.url = url
    urlbox.date = datetime.datetime.now()
    shorted = urlbox.shorted_url
    db.put(urlbox)
    info=[]
    info.append(shorted)
    info.append(urlbox.date)
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
    query = db.Query(UrlBox).filter('shorted_url = ',shorted_url).filter('active = ', True)
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
            return True
        else:
            return False
    except:
        error = str(sys.exc_info()[0])
        print error

def getDomainService(name_domain):
    '''
    grab the name of domain service to build a shorted url
    
    Params 
        name_domain - a valid name of domain : string 
    
    Return 
        domain - the association name of server : string    
        
    '''
    domain = db.Query(Domain).filter('name_domain = ',name_domain).get()
    return domain.shorted_name
