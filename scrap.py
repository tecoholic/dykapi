'''
This File scraps the DYK hooks and stores the data in the datastore.
'''
import os
import urllib
import codecs

from datetime import date

import BeautifulSoup

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.appi import urlfetch


class Hook(db.Model):
    sno = db.IntegerProperty()
    iden = db.StringProperty()
    title = db.StringProperty()
    link = db.StringProperty()
    content = db.TextProperty()


class  ScraperHandler(webapp.RequestHandler):
    def get(self):
        ''' new Scrapper that would scarp image data along with it '''
        #TODO------ open the DB here ---
        sno = 1  #FIXME the serial number should start from last datastore value

        url = "http://en.wikipedia.org/wiki/Wikipedia:Recent_additions/" + pmonth()
        result = urlfetch.fetch(url, headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup.BeautifulSoup(result.content)
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
            #hookfile.write(str(sno)+","+iden+","+title+","+link+","+content+"\n")
            print sno,title
            sno += 1
        #TODO-------- write to the dataStore here ---- 

    def pmonth():
        ''' This funtion computes the previous month and returns the string 
        /year/month '''
        today = date.today()
        day = today.day
        month = today.month
        year = today.year
        if month == 1:
            month = 12
            year = year - 1
        else:
            month = month - 1
        yester = date(year,month,day)
        return date.strftime("%Y/%B")


def main():
    application = webapp.WSGIApplication([('/task/scraphooks', ScraperHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
