#coding:utf-8

from django import template
from datetime import datetime
from blog.views import getCommentNum

register = template.Library()

class showCommentWordsNode2(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        blog = self.sequence.resolve(context, True)
        id = blog.id
        commentNum = getCommentNum(id)
        if commentNum == 0:
            commentWords = ''
        else:
            commentWords = u'%s 条评论' % commentNum
        return commentWords
            
def showCommentWords2(parser, token):
    try:
        tag_name, blog= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(blog)    
    return showCommentWordsNode2(sequence)

class showCommentWordsNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        blog = self.sequence.resolve(context, True)
        id = blog.id
        commentNum = getCommentNum(id)
        if commentNum == 0:
            commentWords = u'等你评论'
        else:
            commentWords = u' %s 条评论' % commentNum
        return commentWords
            
def showCommentWords(parser, token):
    try:
        tag_name, blog= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(blog)    
    return showCommentWordsNode(sequence)

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
            month = "0%s" % month
        if day <10:
            day = "0%s" % day
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
register.tag('showCommentWords', showCommentWords)
register.tag('showCommentWords2', showCommentWords2)
