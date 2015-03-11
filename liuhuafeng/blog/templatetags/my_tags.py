#coding:utf-8

from django import template
from datetime import datetime

register = template.Library()

class showBlogTimeNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        blog = self.sequence.resolve(context, True)

        year = blog.time.year
        month = blog.time.month
        day = blog.time.day
        
        return u'%s年 %s月 %s日' %(year,month,day)
            
def showBlogTime(parser, token):
    try:
        tag_name, blog= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(blog)    
    return showBlogTimeNode(sequence)


class showBlogMDNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        blog = self.sequence.resolve(context, True)

        month = blog.time.month
        day = blog.time.day
        if month < 10:
            month = "0%s' % month
        if day <10:
            day = "0%s' % day
        return u'%s月 %s日' %(month,day)
            
def showBlogMD(parser, token):
    try:
        tag_name, blog= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(blog)    
    return showBlogMDNode(sequence)
    
register.tag('showBlogTime', showBlogTime)
register.tag('showBlogMD', showBlogMD)
