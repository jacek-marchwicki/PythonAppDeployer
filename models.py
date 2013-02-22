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

import sys
try:
  import config
except ImportError:
  sys.stderr.write( "You did not configured application\n")
  sys.exit(1)

from google.appengine.ext import ndb
import messages
import api

class Apps(ndb.Model):
  name = ndb.StringProperty(required=True)
  token = ndb.StringProperty(required=True)
  created_at = ndb.DateTimeProperty(auto_now_add=True)
  updated_at = ndb.DateTimeProperty(auto_now=True)
  owner = ndb.UserProperty(required=True)

  def to_message(self):
    id = self.key.integer_id()
    return messages.AppResponse(name=self.name,
      guid=id,
      created_at=self.created_at.strftime(config.TIME_FORMAT_STRING),
      updated_at=self.created_at.strftime(config.TIME_FORMAT_STRING),
      token=self.token,
      selfLink="%s/apps/%d" % (config.BASE_API_URL, id,),
      appVersionsLink="%s/apps/%d/versions/" % (config.BASE_API_URL, id,),
      )

  def update_from_message(self, message):
   self.name = message.name

  @classmethod
  def from_message(cls, message):
    return cls(name=message.name)

class AppVersions(ndb.Model):
  version = ndb.StringProperty(required=True)
  blob = ndb.BlobKeyProperty(required=True)
  app_id = ndb.IntegerProperty(required=True)
  created_at = ndb.DateTimeProperty(auto_now_add=True)
  updated_at = ndb.DateTimeProperty(auto_now=True)

  def to_message(self):
    id = self.key.integer_id()

    return messages.AppVersionResponse(version=self.version,
      guid=id,
      created_at=self.created_at.strftime(config.TIME_FORMAT_STRING),
      updated_at=self.created_at.strftime(config.TIME_FORMAT_STRING),
      app_download_url="https://%s/download/%s" % (
        config.HOST_NAME, id,),
      selfLink="%s/apps/%d/versions/%d" % (config.BASE_API_URL, self.app_id, id,),
      )

