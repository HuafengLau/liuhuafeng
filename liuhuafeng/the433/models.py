#coding:utf-8

from django.db import models

# Create your models here.

class PassPort(models.Model):
	phone = models.CharField(max_length=15,verbose_name=u'手机号')
	pwd = models.CharField(max_length=30,verbose_name=u'密码')
	nicName = models.CharField(max_length=30,verbose_name=u'昵称')

	def __unicode__(self):
		return u'%s,%s' % (self.nicName, self.phone)

	class Meta:
		ordering = ['phone',]
		verbose_name = u'通行证'
		verbose_name_plural = u'通行证'

class Profile(models.Model):
	passPort = models.ForeignKey(PassPort,verbose_name=u'通行证')
	registerTime = models.DateTimeField(auto_now_add=True,verbose_name=u'注册时间')

	def __unicode__(self):
		return u'%s,%s' % (self.passPort,self.registerTime)

	class Meta:
		ordering = ['passPort',]
		verbose_name = u'用户资料'
		verbose_name_plural = u'用户资料'


class Fund(models.Model):
	code = models.CharField(max_length=6,verbose_name=u'基金代码')
	name = models.CharField(max_length=30,verbose_name=u'基金名称')
	types = models.CharField(max_length=20,verbose_name=u'基金类型')

	cx3years = models.IntegerField(null=True,default=-1,verbose_name=u'晨星3年')
	cx5years = models.IntegerField(null=True,default=-1,verbose_name=u'晨星5年')	
	cxCode = models.CharField(max_length=7,default='',verbose_name=u'晨星地址')

	def __unicode__(self):
		return u'%s,%s' % (self.code, self.name)

	class Meta:
		ordering = ['code',]
		verbose_name = u'基金表'
		verbose_name_plural = u'基金表'


class FundNet(models.Model):
	fund = models.ForeignKey(Fund,verbose_name=u'基金')
	date = models.DateField(verbose_name=u'日期')
	net = models.FloatField(verbose_name=u'净值')
	yields = models.FloatField(verbose_name=u'收益率')

	def __unicode__(self):
		return u'%s,%s' % (self.fund, self.date)

	class Meta:
		ordering = ['fund','date']
		verbose_name = u'基金净值表'
		verbose_name_plural = u'基金净值表'

class UserFundShare(models.Model):
	passPort = models.ForeignKey(PassPort,verbose_name=u'通行证')
	fund = models.ForeignKey(Fund,verbose_name=u'基金')
	types = models.CharField(max_length=20,verbose_name=u'用户理财分类')
	share = models.FloatField(verbose_name=u'份额')

	def __unicode__(self):
		return u'%s,%s' % (self.passPort, self.fund)

	class Meta:
		ordering = ['fund',]
		verbose_name = u'用户基金份额表'
		verbose_name_plural = u'用户基金份额表'

class UserFundProfit(models.Model):
	passPort = models.ForeignKey(PassPort,verbose_name=u'通行证')
	fund = models.ForeignKey(Fund,verbose_name=u'基金')
	date = models.DateField(verbose_name=u'日期')
	todayNet = models.FloatField(verbose_name=u'当日净值',default=0.0)
	beforeDayNet = models.FloatField(verbose_name=u'前一日净值',default=0.0)
	share = models.FloatField(verbose_name=u'份额',default=0.0)
	yields = models.FloatField(verbose_name=u'当日收益率',default=0.0)
	profit = models.FloatField(verbose_name=u'当日收益')
	totalAmount = models.FloatField(verbose_name=u'前一日总金额')

	def __unicode__(self):
		return u'%s,%s' % (self.passPort, self.date)

	class Meta:
		ordering = ['passPort','date']
		verbose_name = u'用户基金收益表'
		verbose_name_plural = u'用户基金收益表'

class UserFundOldProfit(models.Model):
	passPort = models.ForeignKey(PassPort,verbose_name=u'通行证')
	fund = models.ForeignKey(Fund,verbose_name=u'基金')
	year = models.IntegerField(null=True,verbose_name=u'年')
	profit = models.FloatField(verbose_name=u'今年历史收益')

	def __unicode__(self):
		return u'%s,%s' % (self.passPort, self.fund)

	class Meta:
		ordering = ['passPort','fund','year']
		verbose_name = u'用户基金历史收益表'
		verbose_name_plural = u'用户基金历史收益表'

class UserDayProfit(models.Model):
	"""docstring for UserDayProfit"""
	passPort = models.ForeignKey(PassPort,verbose_name=u'通行证')
	date = models.DateField(verbose_name=u'日期')
	profit = models.FloatField(verbose_name=u'当日总收益')
	totalAmount = models.FloatField(verbose_name=u'前一日总金额')
	yields = models.FloatField(verbose_name=u'当日总收益率')

	def __unicode__(self):
		return u'%s,%s' % (self.passPort, self.date)

	class Meta:
		ordering = ['passPort','date']
		verbose_name = u'用户每日收益表'
		verbose_name_plural = u'用户每日收益表'


