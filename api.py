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


from google.appengine.ext import endpoints
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from protorpc import remote
import messages
import models
from Crypto import Random
import base64


@endpoints.api(name='appdeployer',version='v1',
  audiences=config.CLIENT_IDS+[endpoints.API_EXPLORER_CLIENT_ID],
  allowed_client_ids=config.CLIENT_IDS+[endpoints.API_EXPLORER_CLIENT_ID],
  hostname=config.HOST_NAME,
  scopes=["https://www.googleapis.com/auth/userinfo.email",],
  description='App Deployer API')
class AppDeployerApi(remote.Service):

  def get_user(self):
    current_user = endpoints.get_current_user()
    if current_user is None:
      raise endpoints.UnauthorizedException("Invalid token.")
    return current_user


  @endpoints.method(messages.AppListRequest,
    messages.AppListResponse,
    name='apps.list', path='apps', http_method='GET')
  def apps_list(self, request):
    current_user = self.get_user()
    query = models.Apps.query()
    query = query.filter(models.Apps.owner == current_user)
    cursor = Cursor(urlsafe=request.next_token)
    entities, next_cursor, more = query.fetch_page(request.limit,
        start_cursor=cursor)
    next_token = None
    if more and next_cursor:
      next_token = next_cursor.urlsafe()
    items = [entity.to_message() for entity in entities]
    return messages.AppListResponse(items=items,
        next_token=next_token)

  @endpoints.method(messages.AppInsertRequest,
    messages.AppResponse,
    name='apps.insert', path='apps', http_method='POST')
  def apps_insert(self, request):
    current_user = self.get_user()
    entity = models.Apps.from_message(request)
    token = Random.new().read(32)
    entity.token = base64.b64encode(token)
    entity.owner = current_user
    entity.put()
    return entity.to_message()

  def get_app_by_id(self, guid):
    current_user = self.get_user()
    app = models.Apps.get_by_id(guid)
    if app is None:
      raise endpoints.NotFoundException("Not found entity")
    if app.owner != current_user:
      raise endpoints.NotFoundException("Not found entity")
    return app

  def get_app_version_by_id(self, parent, guid):
    app_version = models.AppVersions.get_by_id(guid, parent=parent)
    if app_version is None:
      raise endpoints.NotFoundException("Not found entity")
    return app_version

  @endpoints.method(messages.AppPatchRequest,
    messages.AppResponse,
    name='apps.patch', path='apps/{guid}', http_method='PUT')
  def apps_patch(self, request):
    entity = self.get_app_by_id(request.guid)
    entity.update_from_message(request)
    entity.put()
    return entity.to_message()

  @endpoints.method(messages.AppGetRequest,
    messages.AppResponse,
    name='apps.get', path='apps/{guid}', http_method='GET')
  def apps_get(self, request):
    entity = self.get_app_by_id(request.guid)
    return entity.to_message()


  @endpoints.method(messages.UploadInsertRequest,
    messages.UploadResponse,
    name='apps.upload.insert', path='uploads', http_method="POST")
  def uploads_insert(self, request):
    upload_url = blobstore.create_upload_url('/upload',
        max_bytes_per_blob=config.MAXIMAL_FILE_SIZE,
        gs_bucket_name=config.GS_BUCKET_NAME)
    return messages.UploadResponse(
        upload_url=upload_url)

  @endpoints.method(messages.AppVersionListRequest,
      messages.AppVersionListResponse,
      name='apps.versions.list', path='apps/{app_guid}/versions',
      http_method="GET")
  def app_versions_list(self, request):
    entity = self.get_app_by_id(request.app_guid)

    query = models.AppVersions.query(ancestor=entity.key)
    cursor = Cursor(urlsafe=request.next_token)
    entities, next_cursor, more = query.fetch_page(request.limit,
        start_cursor=cursor)
    next_token = None
    if more and next_cursor:
      next_token = next_cursor.urlsafe()
    items = [entity.to_message() for entity in entities]
    return messages.AppVersionListResponse(items=items,
        next_token=next_token)


  @endpoints.method(messages.AppVersionGetRequest,
      messages.AppVersionResponse,
      name='apps.versions.get', path='apps/{app_guid}/versions/{guid}',
      http_method="GET")
  def app_versions_get(self, request):
    app = self.get_app_by_id(request.app_guid)
    app_version = self.get_app_version_by_id(app.key, request.guid)
    return app_version.to_message()

application = endpoints.api_server([AppDeployerApi,],
  restricted=False)
