'''
This File scraps the DYK hooks and stores the data in the datastore.
'''
import os
import urllib
import codecs

import BeautifulSoup

import BeautifulSoup

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from django.utils import simplejson


class Permission(db.Model):
    text = db.TextProperty()
    id = db.StringProperty()
    link = db.StringProperty()


class  ScraperHandler(webapp.RequestHandler):
    def get(self):
    ''' new Scrapper that would scarp image data along with it '''
    #------ open the DB here ---
    sno = 1  #the serial number should start from last datastore value

    #------- fetch remote url for "html" -------
    html = open(os.path.join(directory,fil), 'r')
    soup = BeautifulSoup.BeautifulSoup(html.read())
    hooklis  = soup.findAll("li",
                            attrs={"style":"-moz-float-edge: content-box"})
    for index,hook in enumerate(hooklis):
        try:
            link = hook.b.a["href"]
        except TypeError:
            link = hook.find("a")["href"]
        link = link.replace("/wiki/","").replace(",",";")
        title = urllib.unquote(unicode(link).encode('ascii')).decode('utf-8')
        title = " ".join(title.split('_')).replace(",",";")
        content = unicode(hook).replace(",",";")
        iden = fil.replace(".html","-")+str(index)
        hookfile.write(str(sno)+","+iden+","+title+","+link+","+content+"\n")
        print sno,title
        sno += 1
    #-------- write to the dataStore here ---- 

def main():
    application = webapp.WSGIApplication([('/task/scraphooks', ScraperHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
