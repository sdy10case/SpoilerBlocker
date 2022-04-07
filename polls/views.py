# Copyright 2015 Google Inc.
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

from django.shortcuts import render
import json
from .models import Content, Request
from django.http import JsonResponse , HttpResponse ####
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def get_content_list(request, url):
    content_list = []
    content_dict = {}
    for content in Content.objects : 
        if content.url == url :
            content_identifier = content.identifier
            content_reason = content.reason
            content_isblocked = content.isblocked
            record = {"identifer":content_identifier, "reason":content_reason,"isBlocked":content_isblocked}
            content_list.append(record)
    content_dict["content"] = content_list


    return JsonResponse(content_dict)
@csrf_exempt
def content(request):
    if request.method == 'POST':
        user_role= request.POST.get('user_role')
        url= request.POST.get('url')
        identifier= request.POST.get('identifier')
        reason = request.POST.get('reason')
        placeholder = request.POST.get('placeholder')
        isblocked = request.POST.get('isblocked')
        newcontent = Content(user_role=user_role, url=url, identifier=identifier, reason=reason, placeholder=placeholder, isblocked=isblocked)
        newcontent.save()
        data = {'user_role':user_role, 'url':url, 'identifier':identifier, 'reason':reason, 'isblocked':isblocked, 'placeholder':placeholder }
        print(data)
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Hello, world. You're at the content index.")
