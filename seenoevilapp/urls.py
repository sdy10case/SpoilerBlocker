from .import views
from django.urls import  path
app_name = 'seenoevilapp'
urlpatterns = [
    path('<str:url>', views.get_content_list, name='get_content_list'),
]
