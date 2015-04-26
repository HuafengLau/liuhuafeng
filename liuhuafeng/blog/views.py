#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from blog.models import Blog
import urllib2,json

hidden = ['compareThree','Discover']

def getCommentNum(id):
    duoshuo_url = 'http://api.duoshuo.com/threads/counts.json?short_name=liuhuafeng&threads=%s' % id
    try:
        web = urllib2.urlopen(duoshuo_url)
        content = web.read()
        info = json.loads(content)
        id_s = '%s' % id
        num = info['response'][id_s]['comments']
        return num 
    except:
        return 0
    

def home(request):                 
    ten_blogs = Blog.objects.exclude(title__in = hidden).order_by('-time')[:20]
    return render_to_response('home.html',locals(),
        context_instance=RequestContext(request))
        
def about(request):
    blog = Blog.objects.get(title='aboutMe')
    return render_to_response('about.html',locals(),
        context_instance=RequestContext(request))
        
def discover(request):
    blog = Blog.objects.get(title='Discover')
    return render_to_response('discover.html',locals(),
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