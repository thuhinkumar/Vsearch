from django.conf.urls import url, include 
from django.contrib import admin
from django.urls import path, re_path
from visualsearch.views import *

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url('^home', Main, name='Visual Search'),
]