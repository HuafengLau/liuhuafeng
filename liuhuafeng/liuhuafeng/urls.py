from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from blog.views import home,about,contents

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'liuhuafeng.views.home', name='home'),
    
    (r'^$', home),
    url(r'^about/', about),
    url(r'^contents/', contents),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #(r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
