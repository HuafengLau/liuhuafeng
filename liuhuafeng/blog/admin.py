#coding:utf-8

from django.contrib import admin
from blog.models import Part, Tag, Blog


class PartAdmin(admin.ModelAdmin):
    """docstring for PartAdmin"""
    list_display = ('Epart', 'Cpart')
    list_filter = ('Epart', 'Cpart')
    ordering = ('Epart', )
    
class TagAdmin(admin.ModelAdmin):
    """docstring for TagAdmin"""
    list_display = ('Etag', 'Ctag')
    list_filter = ('Etag', 'Ctag')
    ordering = ('Etag', )

class BlogAdmin(admin.ModelAdmin):
    """docstring for BlogAdmin"""
    list_display = ('title', 'time','part')
    list_filter = ('time', 'part','tag')
    ordering = ('time', )
    
admin.site.register(Part, PartAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)