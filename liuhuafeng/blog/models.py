#coding:utf-8
from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100,blank=True,verbose_name=u'标题')
    text = models.TextField(null=True,blank=True,verbose_name=u'文本')
	time = models.DateTimeField(auto_now_add=True,verbose_name=u'发表时间')
	
	part = models.ForeignKey(Part, null=True,blank=True,verbose_name=u'分类')
	tag = models.ManyToManyField(Tag, null=True,blank=True,verbose_name=u'标签')
    
    def __unicode__(self):
        return '%s' % (self.id)
    
    class Meta:
        ordering = ['time',]
        verbose_name = u'文章'
        verbose_name_plural = u'文章'
		
class Part(models.Model):
    Epart = models.CharField(max_length=30,null=True,verbose_name=u'英文分类')
    Cpart = models.CharField(max_length=30,null=True,verbose_name=u'中文分类')
    
    def __unicode__(self):
        return '%s' % (self.Epart)
    
    class Meta:
        ordering = ['Epart',]
        verbose_name = u'分类'
        verbose_name_plural = u'分类'
		
class Tag(models.Model):
    Etag = models.CharField(max_length=30,null=True,verbose_name=u'英文标签')
    Ctag = models.CharField(max_length=30,null=True,verbose_name=u'中文标签')
    
    def __unicode__(self):
        return '%s' % (self.Etag)
    
    class Meta:
        ordering = ['Etag',]
        verbose_name = u'标签'
        verbose_name_plural = u'标签'		