#coding:utf-8

from django.contrib import admin

# Register your models here.
from the433.models import *

class PassPortAdmin(admin.ModelAdmin):
    """docstring for PassPortAdmin"""
    list_display = ('phone','nicName')
    list_filter = ('phone','nicName')
    ordering = ('phone',)

admin.site.register(PassPort, PassPortAdmin)

class ProfileAdmin(admin.ModelAdmin):
    """docstring for ProfileAdmin"""
    list_display = ('passPort','registerTime')
    list_filter = ('passPort',)
    ordering = ('passPort','registerTime')

admin.site.register(Profile, ProfileAdmin)


class FundAdmin(admin.ModelAdmin):
    """docstring for FundAdmin"""
    list_display = ('code','name','types','cx3years','cx5years','cxCode')
    list_filter = ('code','name','types','cx3years','cx5years')
    ordering = ('code','types','cx3years','cx5years')

admin.site.register(Fund, FundAdmin)

class FundNetAdmin(admin.ModelAdmin):
    """docstring for FundNetAdmin"""
    list_display = ('fund','date','net','yields')
    list_filter = ('fund','date')
    ordering = ('fund','date','net','yields')

admin.site.register(FundNet, FundNetAdmin)

class UserFundShareAdmin(admin.ModelAdmin):
    """docstring for UserFundShareAdmin"""
    list_display = ('passPort','fund','share')
    list_filter = ('passPort','fund')
    ordering = ('passPort','fund','share')

admin.site.register(UserFundShare, UserFundShareAdmin)

class UserFundProfitAdmin(admin.ModelAdmin):
    """docstring for UserFundProfitAdmin"""
    list_display = ('passPort','fund','date','profit','yields','totalAmount','todayNet','beforeDayNet','share')
    list_filter = ('passPort','date')
    ordering = ('passPort','fund','date')

admin.site.register(UserFundProfit, UserFundProfitAdmin)

class UserFundOldProfitAdmin(admin.ModelAdmin):
    """docstring for UserFundOldProfitAdmin"""
    list_display = ('passPort','fund','year','profit')
    list_filter = ('passPort','fund','year')
    ordering = ('passPort','fund','year')

admin.site.register(UserFundOldProfit, UserFundOldProfitAdmin)

class UserDayProfitAdmin(admin.ModelAdmin):
    """docstring for UserDayProfitAdmin"""
    list_display = ('passPort','date','profit','totalAmount','yields')
    list_filter = ('passPort','date')
    ordering = ('passPort','date','profit','totalAmount','yields')

admin.site.register(UserDayProfit, UserDayProfitAdmin)

class VersionAdmin(admin.ModelAdmin):
    """docstring for UserDayProfitAdmin"""
    list_display = ('name','date','isForced','title','content')
    list_filter = ('name','date','isForced')
    ordering = ('name','date','isForced')

admin.site.register(Version, VersionAdmin)


