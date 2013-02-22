#! /usr/bin/env python
# -*- coding: utf-8 -*-
#   Copyright 2013 Jacek Marchwicki <jacek.marchwicki@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import webapp2
from google.appengine.ext.webapp import blobstore_handlers
import models

import jinja2
import os

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

  def post(self):
    upload_files = self.get_uploads('file')
    blob_info = upload_files[0]
    app_guid = int(self.request.get('app_guid'))
    token = self.request.get('token')
    version= self.request.get('version')
    
    entity = models.Apps.get_by_id(app_guid)
    if entity is None:
      self.response.write('Could not find page!')
      self.response.set_status(404)
      return
    if entity.token != token:
      self.response.write('Invalid token!')
      self.response.set_status(401)
      return

    entity_id = entity.key.integer_id()

    app_version = models.AppVersions(parent=entity.key)
    app_version.version = version
    app_version.blob = blob_info.key()
    app_version.app_id = entity_id
    app_version.put()
    app_version_id = app_version.key.integer_id()
    self.response.write("OK")
    self.response.set_status(200)

app = webapp2.WSGIApplication(
    [
      ('/', MainPage),
      ('/upload', UploadHandler),
    ],
    debug=True)
