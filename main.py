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

import BeautifulSoup

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from django.utils import simplejson

import dehtml

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
        number = str(random.randint(0,500))
        query = "SELECT * FROM Permission WHERE id='2011-April-"+number+"'"
        hook  = db.GqlQuery(query)
        soup = BeautifulSoup.BeautifulSoup(hook[0].text.replace(";", ","))
        ash = soup.findAll("a")
        ashlinks = []
        for a in ash:
            ashlinks.append("http://en.wikipedia.org"+a["href"])
        pageurl = "http://en.wikipedia.org/wiki/"+hook[0].link.replace(";", ",")
        tex = dehtml.dehtml(hook[0].text)
        tex = tex.replace("... that ","",1).replace(';',',')
        texlt = tex.split(" ",1)
        tex = texlt[0].capitalize()+" "+texlt[1]
        
        if format == "json":
            self.response.headers['Content-Type'] = 'text/plain'
            jsonData = {"title" : urllib2.unquote(hook[0].link.replace(";", ",")),
                        "text" : unicode(tex),
                        "pageurl" : pageurl,
                        "metaurls": ashlinks}
            self.response.out.write(simplejson.dumps(jsonData))
        else:
            self.response.out.write("Incompatible format or No format specified!")


def main():
    application = webapp.WSGIApplication([('/', HomeHandler),
                                          ('/api/', ApiHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
