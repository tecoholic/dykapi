#!/usr/bin/env python
#
# Copyright Arunmozhi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import urllib2
import random

from xml.dom.minidom import Document

import BeautifulSoup

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from django.utils import simplejson

import dehtml
from dict2xml import dict2xml

class Test(db.Model):
    lis = db.TextProperty()

class Permission(db.Model):
    text = db.TextProperty()
    id = db.StringProperty()
    link = db.StringProperty()


class HomeHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<h1>DYK API</h1>')

class ApiHandler(webapp.RequestHandler):
    def get(self):
        format = self.request.get("format")
        hook  = db.GqlQuery(self.__queryString())
        #find a way to redo until data is returned
        while(hook.count() == 0):
                hook = db.GqlQuery(self.__queryString())
        soup = BeautifulSoup.BeautifulSoup(hook[0].text.replace(";", ","))
        ash = soup.findAll("a")
        ashlinks = []
        for a in ash:
            metadict = {'metaurl' : "http://en.wikipedia.org"+a["href"],
                        'metatext' : a.text }
            ashlinks.append(metadict)
        tex = dehtml.dehtml(hook[0].text)
        tex = tex.replace("... that ","",1).replace(';',',').rstrip("?")
        texlt = tex.split(" ",1)
        tex = texlt[0].capitalize()+" "+texlt[1]
        responseData = {"response": [{"hook":{
                    "title" : hook[0].link.replace(";", ","),
                    "text" : tex,
                    "metadata": ashlinks}}]}
        if format == "json":
            self.ReturnJSON(responseData)
        elif format == "xml":
            self.ReturnXML(responseData)
        else:
            self.response.out.write("Incompatible format or No format specified!")

    def ReturnJSON(self, data):
        ''' the function gets the data as a dictionary and returns the JSON object '''
        self.response.headers["Content-Type"] = 'application/json'
        self.response.out.write(simplejson.dumps(data))
    
    def ReturnXML(self, data):
        ''' the function gets the data dict and returns the XML response '''
        xmltxt = dict2xml(data)
        self.response.headers["Content-Type"] = 'text/xml'
        self.response.out.write(xmltxt.doc.toxml('utf-8'))
        
    def __queryString(self):
        ''' This fucntion generates a query string by selecting a random year, month and number '''
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 'November', 'December']
        year = random.randint(2004,2011)
        month = months[random.randint(0,11)]
        hook = random.randint(0,1200)
        
        query = "SELECT * FROM Permission WHERE id='"+str(year)+"-"+month+"-"+str(hook)+"'"
        return query

def main():
    application = webapp.WSGIApplication([('/', HomeHandler),
                                          ('/api/', ApiHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
