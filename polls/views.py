# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.shortcuts import render
import json
from .models import Content, Createrequest, Priviligeduser, Reportrequest, Baseuser
from django.http import JsonResponse , HttpResponse ####
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import datetime
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
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            content_object = json.loads(request.body)
            newcontent = Content(user_role=content_object['user_role'], url=content_object['url'], identifier=content_object['identifier'], reason=content_object['reason'], placeholder=content_object['placeholder'], isblocked=content_object['isblocked'])
            newcontent.save()
            #data = {'user_role':user_role, 'url':url, 'identifier':identifier, 'reason':reason, 'isblocked':isblocked, 'placeholder':placeholder }
            #eturn JsonResponse(data, safe=False)
        elif request.method == 'PUT':
            content_update = json.loads(request.body)
            c = Content.objects.get(pk=content_update['c_id'])
            c.isblocked = content_update['isblocked']
            c.save()
        return HttpResponse("Hello, world." + content_object['isblocked'] + "You're at the content index.") 
    else:
        return HttpResponse("Hello, world. You're at the content2 index.") 
def request(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        request_object = json.loads(request.body)
        if request_object['type'] == "request": 
            newrequest = Createrequest(baseuserid=request_object['baseuserid'], user_role=request_object['user_role'], url=request_object['url'], identifier=request_object['identifier'], reason=request_object['reason'], placeholder=request_object['placeholder'], isresolved=request_object['isresolved'], priviledgeduserid=request_object['priviledgeduserid'])
            newrequest.save()
        else:
            newrequest = Reportrequest(baseuserid=request_object['baseuserid'], user_role=request_object['user_role'], url=request_object['url'], identifier=request_object['identifier'], reason=request_object['reason'], placeholder=request_object['placeholder'], isresolved=request_object['isresolved'], c=request_object['c'], priviledgeduserid=request_object['priviledgeduserid'])
            newrequest.save()
        #data = {'user_role':user_role, 'url':url, 'identifier':identifier, 'reason':reason, 'isblocked':isblocked, 'placeholder':placeholder }
        #eturn JsonResponse(data, safe=False)
        return HttpResponse("Hello, world." + request_object['user_role'] + "You're at the request index.") 
    else:
        return HttpResponse("Hello, world. You're at the content2 index.") 
def newuser(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_object = json.loads(request.body)
        if user_object['user_role'] == "baseuser":
            newuser = Baseuser(name=user_object['name'], surname=user_object['surname'], password=user_object['password'], email=user_object['email'], maxcontent = 5, dailycontentmarked= 0, maxmet = False)
            newuser.save()
        else:
            newpriviligeduser = Priviligeduser(name=user_object['name'], surname=user_object['surname'], password=user_object['password'], email=user_object['email'], user_role=user_object['user_role'])
            newpriviligeduser.save()
        #data = {'user_role':user_role, 'url':url, 'identifier':identifier, 'reason':reason, 'isblocked':isblocked, 'placeholder':placeholder }
        #eturn JsonResponse(data, safe=False)
        return HttpResponse("Hello, world." + user_object['user_role'] + "You're at the request index.") 
    else:
        return HttpResponse("Hello, world. You're at the content2 index.") 
def login(request):
    user_object = json.loads(request.body)
    try:
        privuser = Priviligeduser.objects.get(email=user_object['email'], password=user_object['password'])
        data = {'user_role':privuser.user_role, 'priviligeduserid': privuser.priviligeduser}
        return JsonResponse(data, safe=False)
    except Priviligeduser.DoesNotExist:
        baseuser = get_object_or_404(Baseuser, email=user_object['email'], password=user_object['password'])
        if baseuser.reset_limit:
            baseuser.maxmet = False
            baseuser.dailycontentmarked = 0
            data = {'user_role':'baseuser', 'baseuserid': baseuser.userid, 'maxcontent': baseuser.maxcontent, 'dailycontentmarked': baseuser.dailycontentmarked, 'maxmet': baseuser.maxmet}
    return JsonResponse(data, safe=False)


