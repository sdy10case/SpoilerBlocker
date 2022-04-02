from django.shortcuts import render
import json
from .models import Content, Request
from django.http import JsonResponse , HttpResponse ####
# Create your views here.
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