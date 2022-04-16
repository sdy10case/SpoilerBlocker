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
from .models import Content, Createrequest, Priviligeduser, Reportrequest, Baseuser, Account
from django.http import JsonResponse , HttpResponse ####
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.shortcuts import redirect

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def get_content_list(request, url):
    content_list = []
    content_dict = {}
    for content in Content.objects.all() : 
        if content.url == url and content.isblocked == True:
            content_id = content.c_id
            content_identifier = content.identifier
            content_placeholder = content.placeholder
            content_reason = content.reason
            content_isblocked = content.isblocked
            record = {"c_id": content_id, "identifier":content_identifier, "placeholder":content_placeholder,"isBlocked":content_isblocked, "reason": content_reason}
            content_list.append(record)
    content_dict["content"] = content_list


    return JsonResponse(content_dict)
def view_content_list(request, url_inp):
    if request.method == "POST":
        return redirect(url_inp)
    content_exists = Content.objects.all().filter(url = url_inp)
    context = {'content_exists' : content_exists, 'url_inp' : url_inp}
    return render(request, 'polls/content.html', context)
def view_request_list(request, puid):
    if request.method == "GET":
        create_request_exists = Createrequest.objects.all().filter(isresolved = False)
        report_request_exists = Reportrequest.objects.all().filter(isresolved = False)
        context = {'create_request_exists' : create_request_exists, 'report_request_exists' : report_request_exists, 'puid' : puid}
        return render(request, 'polls/request.html', context)
    else:
        privuser = Priviligeduser.objects.get(pk = puid)
        for requests in Createrequest.objects.all().filter(isresolved = False):
            approve = request.POST.get('approve_create_request' + str(requests.r_id), False)
            disapprove = request.POST.get('disapprove_create_request' + str(requests.r_id), False)
            if approve and disapprove:
                return render(request, 'polls/request.html', {
                'error_message': "Cannot select both approve and disapprove for a request.",
                })
            elif approve:
                requests.isresolved = True
                requests.save()
                try:
                    content= Content.objects.get(identifier=requests.identifier)
                    content.isblocked = True
                    content.save()
                except Content.DoesNotExist:
                    newcontent = Content(user_role=requests.user_role, url=requests.url, identifier=requests.identifier, reason=requests.reason, placeholder=requests.placeholder, isblocked=True, create_r_id=requests, priviligeduserid = privuser)
                    newcontent.save()
            elif disapprove:
                requests.isresolved = True
                requests.save()
        for requests in Reportrequest.objects.all().filter(isresolved = False):
            approve = request.POST.get('approve_report_request' + str(requests.r_id), False)
            disapprove = request.POST.get('disapprove_report_request' + str(requests.r_id), False)
            if approve and disapprove:
                return render(request, 'polls/request.html', {
                'error_message': "Cannot select both approve and disapprove for a request.",
                })
            elif approve:
                requests.isresolved = True
                requests.save()
                try:
                    content= Content.objects.get(identifier=request.identifier)
                    content.isblocked = False
                    content.reason = requests.reason
                    content.placeholder = requests.placeholder
                    content.save()
                except Content.DoesNotExist:
                    continue
            elif disapprove:
                requests.isresolved = True
                requests.save()
        return HttpResponse('Form submitted successfully')
def view_user_list(request):
    if request.method == "GET":
        user_exists = Baseuser.objects.all()
        mod_exists = Priviligeduser.objects.all().filter(user_role = "moderator")
        admin_exists = Priviligeduser.objects.all().filter(user_role = "admin")
        context = {'user_exists' : user_exists, 'mod_exists' : mod_exists, 'admin_exists' : admin_exists}
        return render(request, 'polls/users.html', context)
    else:
        for users in Baseuser.objects.all():
            to_mod = request.POST.get('baseuser_to_mod' + str(users.userid), False)
            to_admin = request.POST.get('baseuser_to_admin' + str(users.userid), False)
            delete = request.POST.get('delete_baseuser' + str(users.userid), False)
            if (to_mod and to_admin) or (to_mod and delete) or (to_admin and delete):
                return render(request, 'polls/users.html', {
                'error_message': "Cannot select multiple options per user.",
                })
            elif to_mod:
                newmod = Priviligeduser(user_role="moderator", name = users.name, surname = users.surname, email=users.email, password = users.password)
                newmod.save()
                users.delete()
            elif to_admin:
                newadmin = Priviligeduser(user_role="admin", name = users.name, surname = users.surname, email=users.email, password = users.password)
                newadmin.save()
                users.delete()
            elif delete:
                users.delete()
        for users in Priviligeduser.objects.all().filter(user_role = "moderator"):
            to_base = request.POST.get('mod_to_baseuser' + str(users.userid), False)
            to_admin = request.POST.get('mod_to_admin' + str(users.userid), False)
            delete = request.POST.get('delete_mod' + str(users.userid), False)
            if (to_base and to_admin) or (to_base and delete) or (to_admin and delete):
                return render(request, 'polls/users.html', {
                'error_message': "Cannot select multiple options per user.",
                })
            elif to_base:
                newbase = Baseuser(user_role="baseuser", name = users.name, surname = users.surname, email=users.email, password = users.password, maxcontent = 5, dailycontentmarked= 0, maxmet = False, maxmetdate=timezone.now())
                newbase.save()
                users.delete()
            elif to_admin:
                newadmin = Priviligeduser(user_role="admin", name = users.name, surname = users.surname, email=users.email, password = users.password)
                newadmin.save()
                users.delete()
            elif delete:
                users.delete()
        for users in Priviligeduser.objects.all().filter(user_role = "admin"):
            to_base = request.POST.get('admin_to_baseuser' + str(users.userid), False)
            to_mod = request.POST.get('admin_to_mod' + str(users.userid), False)
            delete = request.POST.get('delete_admin' + str(users.userid), False)
            if (to_base and to_admin) or (to_base and delete) or (to_admin and delete):
                return render(request, 'polls/users.html', {
                'error_message': "Cannot select multiple options per user.",
                })
            elif to_base:
                newbase = Baseuser(user_role="baseuser", name = users.name, surname = users.surname, email=users.email, password = users.password, maxcontent = 5, dailycontentmarked= 0, maxmet = False, maxmetdate=timezone.now())
                newbase.save()
                users.delete()
            elif to_mod:
                newadmin = Priviligeduser(user_role="moderator", name = users.name, surname = users.surname, email=users.email, password = users.password)
                newadmin.save()
                users.delete()
            elif delete:
                users.delete()
        return HttpResponse('Form submitted successfully')
@csrf_exempt
def content(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            content_object = json.loads(request.body)
            try:
                content= Content.objects.get(identifier=content_object['identifier'])
                content.isblocked = True
                content.reason = content_object['reason']
                content.placeholder = content_object['placeholder']
                content.save()
            except Content.DoesNotExist:
                newcontent = Content(user_role=content_object['user_role'], url=content_object['url'], identifier=content_object['identifier'], reason=content_object['reason'], placeholder=content_object['placeholder'], isblocked=content_object['isblocked'])
                newcontent.save()
        elif request.method == 'PUT':
            content_update = json.loads(request.body)
            c = Content.objects.get(pk=content_update['c_id'])
            c.isblocked = False
            c.save()
        data = {'raw':'Success'}
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Hello, world. You're at the content2 index.") 
def request(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        request_object = json.loads(request.body)
        user = Baseuser.objects.get(pk=request_object['baseuserid'])
        if not user.maxmet:
            user.dailycontentmarked += 1
            if user.dailycontentmarked == user.maxcontent:
                user.maxmet = True
                user.maxmetdate=timezone.now()
            user.save()
        else:
            if not user.reset_limit():
                data = {'raw' : 'maxmet'}
                return JsonResponse(data, safe=False)
            user.dailycontentmarked = 1
            user.maxmet = False
            user.save()   
        if request_object['type'] == "create": 
            for requests in Createrequest.objects.all() : 
                if requests.identifier == request_object["identifier"] and requests.isresolved == False :
                    data = {'raw':'Already Exists'}
                    return JsonResponse(data, safe=False)
                elif requests.identifier == request_object["identifier"] and requests.isresolved == True :
                    requests.isresolved = False
                    requests.baseuserid = user
                    requests.reason = request_object["reason"]
                    requests.placeholder = request_object["placeholder"]
                    requests.save()
                    data = {'raw': 'Updated Existing request'}
                    return JsonResponse(data, safe=False)
            newrequest = Createrequest(baseuserid=user, user_role=request_object['user_role'], url=request_object['url'], identifier=request_object['identifier'], reason=request_object['reason'], placeholder=request_object['placeholder'], isresolved=False)
            newrequest.save()
        else:
            for requests in Reportrequest.objects.all() : 
                if requests.identifier == request_object["identifier"] and requests.isresolved == False :
                    data = {'raw':'Already Exists'}
                    return JsonResponse(data, safe=False)
                elif requests.identifier == request_object["identifier"] and requests.isresolved == True :
                    requests.isresolved = False
                    requests.baseuserid = user
                    requests.reason = request_object["reason"]
                    requests.save()
                    data = {'raw': 'Updated Existing request'}
                    return JsonResponse(data, safe=False)
            newrequest = Reportrequest(baseuserid=user, user_role=request_object['user_role'], url=request_object['url'], identifier=request_object['identifier'], reason=request_object['reason'], placeholder=request_object['placeholder'], isresolved=False, c=request_object['c'])
            newrequest.save()
        data = {'raw':'Success'}
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Hello, world. You're at the content2 index.") 
def register(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_object = json.loads(request.body)
        for users in Baseuser.objects.all() : 
            if users.email == user_object['email'] :
                data = {'raw':'Failure'}
                return JsonResponse(data, safe=False)
        for users in Priviligeduser.objects.all() : 
            if users.email == user_object['email'] :
                data = {'raw':'Failure'}
                return JsonResponse(data, safe=False)
        newuser = Baseuser(name=user_object['name'], surname=user_object['surname'], password=user_object['password'], email=user_object['email'], maxcontent = 5, dailycontentmarked= 0, maxmet = False, maxmetdate=timezone.now())
        newuser.save()
        data = {'raw':'Success'}
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Hello, world. You're at the content2 index.") 
def login(request, email_inp, password_inp):
    try:
        privuser = Priviligeduser.objects.get(email=email_inp)
        if privuser.password == password_inp:
            data = {'user_role':privuser.user_role, 'userid': privuser.userid}
            return JsonResponse(data, safe=False)
        else:
            data = {'raw': 'wrong password'}
            return JsonResponse(data, safe=False)
    except Priviligeduser.DoesNotExist:
        baseuser = get_object_or_404(Baseuser, email=email_inp)
        if baseuser.password != password_inp:
            data = {'raw': 'wrong password'}
            return JsonResponse(data, safe=False)
        if baseuser.reset_limit():
            baseuser.maxmet = False
            baseuser.dailycontentmarked = 0
            baseuser.save()
        data = {'user_role':'baseuser', 'userid': baseuser.userid, 'maxcontent': baseuser.maxcontent, 'dailycontentmarked': baseuser.dailycontentmarked, 'maxmet': baseuser.maxmet}
        return JsonResponse(data, safe=False)


