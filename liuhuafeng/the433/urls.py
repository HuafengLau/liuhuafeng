#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('the433.views',
    url(r'^passport/register/$', 'register', name='register'),
    url(r'^passport/login/$', 'login', name='login'),
    url(r'^fund/useraddfund/$', 'userAddFund', name='userAddFund'),
)