#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('the433.views',
    url(r'^passPort/register/$', 'register', name='register'),
    url(r'^passPort/login/$', 'login', name='login'),
    url(r'^fund/useraddfund/$', 'userAddFund', name='userAddFund'),
)