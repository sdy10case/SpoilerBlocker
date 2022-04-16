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

from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('content/', views.content, name='content'),
    path('request/', views.request, name='request'),
    path('register/', views.register, name='register'),
    path('view_request_list/<int:puid>/', views.view_request_list, name='view_request_list'),
    path('view_content_list/<path:url_inp>/', views.view_content_list, name='view_content_list'),
    path('view_user_list/', views.view_user_list, name='view_user_list'),
    path('login/<str:email_inp>/<str:password_inp>/', views.login, name='login'),
    path('<path:url>/', views.get_content_list, name='get_content_list')
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
