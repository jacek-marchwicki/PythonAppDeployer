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

from protorpc import messages


class AppResponse(messages.Message):
  guid = messages.IntegerField(1, required=True)
  name = messages.StringField(2, required=True)
  token = messages.StringField(6, required=True)
  created_at = messages.StringField(3, required=True)
  updated_at = messages.StringField(4, required=True)
  selfLink = messages.StringField(5, required=True)
  appVersionsLink = messages.StringField(7, required=True)

class AppListResponse(messages.Message):
  items = messages.MessageField(AppResponse, 1, repeated=True)
  next_token = messages.StringField(2, required=False)

class AppListRequest(messages.Message):
  limit = messages.IntegerField(1, default=10, required=False)
  next_token = messages.StringField(2, required=False)

class AppGetRequest(messages.Message):
  guid = messages.IntegerField(1, required=True)

class AppPatchRequest(messages.Message):
  guid = messages.IntegerField(1, required=True)
  name = messages.StringField(2, required=True)

class AppInsertRequest(messages.Message):
  name = messages.StringField(1, required=True)

class UploadResponse(messages.Message):
  upload_url = messages.StringField(1, required=True)

class UploadInsertRequest(messages.Message):
  pass

class AppVersionResponse(messages.Message):
  app_download_url = messages.StringField(1, required=True)
  version = messages.StringField(2, required=True)
  created_at = messages.StringField(3, required=True)
  updated_at = messages.StringField(4, required=True)
  selfLink = messages.StringField(5, required=True)
  guid = messages.IntegerField(6, required=True)

class AppVersionListRequest(messages.Message):
  app_guid = messages.IntegerField(1, required=True)
  limit = messages.IntegerField(2, default=10, required=False)
  next_token = messages.StringField(3, required=False)

class AppVersionGetRequest(messages.Message):
  app_guid = messages.IntegerField(1, required=True)
  guid = messages.IntegerField(2, required=True)

class AppVersionListResponse(messages.Message):
  items = messages.MessageField(AppVersionResponse, 1, repeated=True)
  next_token = messages.StringField(2, required=False)

