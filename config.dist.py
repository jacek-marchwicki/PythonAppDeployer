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

HOST_NAME = "app-deployer.appspot.com"
BASE_API_URL = "https://%s/_ah/api/appdeployer/v1" % HOST_NAME
CLIENT_IDS = ['XXX.apps.googleusercontent.com']
GS_BUCKET_NAME = "YOUR_GOOGLE_STORAGE_BUCKET_NAME"
MAXIMAL_FILE_SIZE = 30*1024*1024
TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'
