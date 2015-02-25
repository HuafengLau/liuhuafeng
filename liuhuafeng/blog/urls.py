#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('blog.views',
    url(r'^(?P<blogId>\d+)/$', 'readBlog', name='readBlog'),
    
)