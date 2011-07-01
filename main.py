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
from google.appengine.api import urlfetch


from google.appengine.ext import db
class Test(db.Model):
    lis = db.TextProperty()

class Hook(db.Model):
    text = db.TextProperty()
    page = db.StringProperty()
    category = db.StringProperty() # Remove Me later
    #projects = db.ListProperty(db.key, default=None)

class HomeHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<h1>DYK API</h1>')

class MakeHandler(webapp.RequestHandler):
    def get(self):
        f = urlfetch.fetch("http://en.wikipedia.org/wiki/Wikipedia:Recent_additions")
        soup = BeautifulSoup.BeautifulSoup(f.content)
        lis  = soup.findAll("li", attrs={"style":"-moz-float-edge: content-box"})
        tet = Test()
        tet.lis = lis.__str__()
        tet.put()
        for li in lis:
            dbhook = Hook()
            try:
                link = li.b.a["href"]
            except TypeError:
                link = li.find("a")["href"]
            dbhook.text = str(li)
            dbhook.page = link.replace("/wiki/","")
            dbhook.category = "June"
            dbhook.put()
        self.response.out.write("Done!")


def main():
    application = webapp.WSGIApplication([('/', HomeHandler),
                                          ('/make', MakeHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
