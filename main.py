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
import BeautifulSoup
import urllib2

from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

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
        hook  = db.GqlQuery("SELECT * FROM Permission WHERE id='2011-April-3'")
        #print type(hook)
        self.response.out.write(hook[0].link)
        #self.response.out.write(hook.text)

def main():
    application = webapp.WSGIApplication([('/', HomeHandler),
                                          ('/api', ApiHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
