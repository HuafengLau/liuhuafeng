#coding:utf-8

from __future__ import absolute_import

from celery import shared_task
from the433.views import updateFundNet, updateUserFundProfit, updateUserProfit
from the433.models import Fund, FundNet, UserFundShare,PassPort
import datetime
import json


#更新每个基金净值，若基金今日净值有更新，随即更新拥有该基金的用户的收益
@shared_task
def dayUpdateFundNet():
	allFund = Fund.objects.all()
	today = datetime.date.today()

	response_data = {}
	#实际尝试更新的基金数
	tryUpdate = 0
	#真正有更新的基金数
	hasUpdate = 0
	#今日净值有更新的基金数
	todayUpdate = 0

	if allFund:
		for fund in allFund:
			try:
				netExist = FundNet.objects.get(fund=fund,date=today)
				pass
			except Exception, e:
				tryUpdate += 1
				result = updateFundNet(fund.code)
				if 'today' in result:
					todayUpdate += 1
					targetFundShre = UserFundShare.objects.filter(fund=fund,share__gt=0.0)
					if targetFundShre:
						for userFundShare in targetFundShre:
							updateUserFundProfit(userFundShare.passPort, today, userFundShare.fund)
					else:
						pass
				else:
					pass
				if result:
					if result.split(',')[0] != '0':
						hasUpdate += 1

		response_data['tryUpdate'] = tryUpdate
		response_data['hasUpdate'] = hasUpdate
		response_data['todayUpdate'] = todayUpdate
		return response_data
	else:
		return 'wrong'

#更新每个用户每个基金的今日收益
@shared_task
def dayUpdateUserFundProfit():
	today = datetime.date.today()
	allUserFundShare = UserFundShare.objects.filter(share__gt=0.0)

	#尝试更新的用户基金个数
	tryUpdate = 0
	#成功更新的用户基金个数
	hasUpdate = 0
	response_data = {}

	if allUserFundShare:
		for userFundShare in allUserFundShare:
			tryUpdate += 1
			if updateUserFundProfit(userFundShare.passPort, today, userFundShare.fund):
				hasUpdate += 1
		response_data['tryUpdate'] = tryUpdate
		response_data['hasUpdate'] = hasUpdate
		return response_data
	else:
		pass


#更新每个用户每天的收益
@shared_task
def dayUpdateUserProfit():
	allUser = PassPort.objects.all()
	today = datetime.date.today()

	#尝试更新的用户基金个数
	tryUpdate = 0
	#成功更新的用户基金个数
	hasUpdate = 0
	response_data = {}

	if allUser:
		for passPort in allUser:
			tryUpdate += 1
			if updateUserProfit(passPort,today):
				hasUpdate += 1
		response_data['tryUpdate'] = tryUpdate
		response_data['hasUpdate'] = hasUpdate
		return response_data
	else:
		pass


#更新每个用户每个基金的昨日收益
@shared_task
def yesterdayUpdateUserFundProfit():
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	allUserFundShare = UserFundShare.objects.filter(share__gt=0.0)

	#尝试更新的用户基金个数
	tryUpdate = 0
	#成功更新的用户基金个数
	hasUpdate = 0
	response_data = {}

	if allUserFundShare:
		for userFundShare in allUserFundShare:
			tryUpdate += 1
			if updateUserFundProfit(userFundShare.passPort, yesterday, userFundShare.fund):
				hasUpdate += 1

		response_data['tryUpdate'] = tryUpdate
		response_data['hasUpdate'] = hasUpdate
		return response_data

	else:
		pass

#更新每个用户昨天的收益
@shared_task
def yesterdayUpdateUserProfit():
	allUser = PassPort.objects.all()
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	
	#尝试更新的用户基金个数
	tryUpdate = 0
	#成功更新的用户基金个数
	hasUpdate = 0
	response_data = {}

	if allUser:
		for passPort in allUser:
			tryUpdate += 1
			if updateUserProfit(passPort,yesterday):
				hasUpdate += 1
		response_data['tryUpdate'] = tryUpdate
		response_data['hasUpdate'] = hasUpdate
		return response_data
	else:
		pass

#用来测试
@shared_task
def doNothing():
	pass
