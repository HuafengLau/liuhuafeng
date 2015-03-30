#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from blog.models import Blog

hidden = ['compareThree',]

def home(request):                 
    ten_blogs = Blog.objects.exclude(title__in = hidden).order_by('-time')[:20]
    return render_to_response('home.html',locals(),
        context_instance=RequestContext(request))
        
def about(request):
    blog = Blog.objects.get(title='aboutMe')
    return render_to_response('about.html',locals(),
        context_instance=RequestContext(request))
        
def contents(request):
    blogs_2015 = Blog.objects.filter(time__year=2015).exclude(title__in = hidden)
    blogs_2014 = Blog.objects.filter(time__year=2014).exclude(title__in = hidden)
    return render_to_response('contents.html',locals(),
        context_instance=RequestContext(request))
               
        
def readBlog(request,blogId):
    blog = Blog.objects.get(id=blogId)
    return render_to_response('readBlog.html',locals(),
        context_instance=RequestContext(request))