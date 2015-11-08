#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import json
#from blog.models import Blog
#import urllib2,json

def register(request):
    if request.method == 'POST':
    	#data=simplejson.loads(request.raw_post_data)
    	if 'phone' in request.POST and 'pwd' in request.POST and 'nicName' in request.POST:
    		phone = request.POST.get('phone')
    		pwd = request.POST.get('pwd')
    		nicName = request.POST.get('nicName')
    		response_data = {}
    		response_data['phone'] = phone
    		response_data['pwd'] = pwd
    		response_data['nicName'] = nicName
    	else：
    		response_data = {}
    		response_data['msg'] = 'error'
    	return HttpResponse(json.dumps(response_data), 
    		content_type='application/json')