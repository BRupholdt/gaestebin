# Copyright 2012 Diwaker Gupta
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

import cgi
import jinja2
import logging
import os
import random
import string
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Paste(db.Model):
    id = db.StringProperty()
    content = db.TextProperty()
    timestamp = date = db.DateTimeProperty(auto_now_add=True)

def gen_random_string(length):
    chars = string.letters + string.digits
    return ''.join(random.choice(chars) for i in xrange(length))

class SavePaste(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        paste = Paste()
        paste.id = gen_random_string(8)
        paste.content = self.request.get('content')
        paste.put()
        self.redirect('/' + paste.id)

class CreatePaste(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        template_values = {}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class ShowPaste(webapp2.RequestHandler):
    def get(self, paste_id):
        query = db.Query(Paste)
        query.filter("id = ", paste_id)
        template_values = {"content": cgi.escape(query.get().content)}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    (r'/', CreatePaste),
    (r'/paste', SavePaste),
    (r'/(\S+)', ShowPaste)
    ])
