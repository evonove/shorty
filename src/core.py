from google.appengine.ext import db
from binding import bind
from models import DomainTable
from models import UrlBox
import time 

def core_classic(url):
    mydomain="www.cerbero.it/"
    dominio = computeDomain(url)
    is_recycle=isReciclable(dominio)
    if is_recycle:
        shorted = recycle(dominio,url)
    else:
        shorted = bind(dominio) 
        url_shortato = mydomain+dominio+shorted
        dt=UrlBox()
        dt.domain = dominio
        dt.url = url 
        dt.shorted_url=url_shortato
        dt.date=time.mktime(time.localtime())
        dt.active = True
        db.put(dt) 
    return shorted
    


def isReciclable(dominio):
    dt=UrlBox()
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
    

def recycle(dominio,url):
    dt=UrlBox()
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    dt = query.fetch(1)[0]
    dt.active=True
    dt.url = url
    dt.date = time.mktime(time.localtime())
    shorted = dt.shorted_url
    db.put(dt)
    return shorted



def computeDomain(url):
    count = 0
    start = 0
    stop = 0
    controllo = 1 

    for c in url:
        if c=='w' and start==0:
                start = count
        elif c=='/' and start>0 :
                stop = count
                break
        else : 
                stop=len(url)
        count = count + 1
        
    if url[0]=='w': 
        dom = url[start+3:stop]
    else:
        dom = url[start+4:stop]

#blocco sul controllo del dominio se in white list concesso 
    if controllo == 1 :
        dom = dom[0:len(dom)-3]
    
    return dom


def whiteList():
    return 1

def main():
    core_classic("http://www.google.it/abc/lod")
    core_classic("http://www.google.it/abc/loa")
    core_classic("http://www.libero.it/ac/lde")
    

     
  
if __name__ == "__main__":
    main()

        