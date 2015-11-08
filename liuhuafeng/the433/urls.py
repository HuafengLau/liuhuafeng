#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('the433.views',
    url(r'^user/register/$', 'register', name='register'),
    #url(r'^user/login/$', 'login', name='login'),
)