# Copyright 2020 Google LLC. All rights reserved.
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

from django.test import Client, TestCase  # noqa: 401
from .models import Content, Request

class PollViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert 'Hello, world' in str(response.content)
    def test_content_upload(self):
        user_role= 'me'
        url= 'www.example.com'
        identifier= 'identifier'
        reason = 'reason'
        placeholder = 'placeholder'
        isblocked = 'True'
        newcontent = Content(user_role=user_role, url=url, identifier=identifier, reason=reason, placeholder=placeholder, isblocked=isblocked)
        newcontent.save()
        content = Content.objects.get(identifier="identifier")
        self.assertEqual(content.url, 'www.example.com')
