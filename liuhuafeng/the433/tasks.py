from __future__ import absolute_import

from celery import shared_task
from the433.views import updateFundNet
from the433.models import Fund,FundNet
import datetime


@shared_task
def add(x, y):
    return x + y

@shared_task
def dayUpdateFundNet():
	allFund = Fund.objects.all()
	today = datetime.date.today()
	for fund in allFund:
		try:
			netExist = FundNet.objects.get(fund=fund,date=today)
		except Exception, e:
			updateFundNet(fund.code)
