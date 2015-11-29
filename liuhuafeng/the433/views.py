#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from the433.models import PassPort,Profile,Fund,FundNet,UserFundShare,UserFundProfit,UserFundOldProfit
from bs4 import BeautifulSoup
import urllib2


def register(request):
    if request.method == 'POST':
    	#data=simplejson.loads(request.raw_post_data)
        response_data = {
            "meta":{
                "code":200,
                "msg":'注册成功'
            },
            "data":""
        }

    	if 'phone' in request.POST and 'pwd' in request.POST and 'nicName' in request.POST:
    		
            phone = request.POST.get('phone')
    		pwd = request.POST.get('pwd')
    		nicName = request.POST.get('nicName')

            try:
                phoneExist = PassPort.objects.get(phone=phone)
                response_data['meta']['code'] = 201
                response_data['meta']['msg'] = '手机号存在'
                
            except Exception, e:
                newPassPort = PassPort(
                    phone = phone,
                    pwd = pwd,
                    nicName = nicName
                    )
                newPassPort.save()

                newProfile = Profile(
                    passPort = newPassPort
                    )
                newProfile.save()
        		response_data['result'] = 'success'
            finally:
                return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')

    	else：
            response_data['meta']['code'] = 202
            response_data['meta']['msg'] = '参数有误'
    	    return HttpResponse(json.dumps(response_data), 
                content_type='application/json')

def login(request):
    if 'phone' in request.POST and 'pwd' in request.POST:
        response_data = {
            "meta":{
                "code":200,
                "msg":'登录成功'
            },
            "data":""
        }
        try:
            phone = request.POST.get('phone')
            pwd = request.POST.get('pwd')
            passPortExist = PassPort.objects.get(phone=phone,pwd=pwd)

        except Exception, e:
            response_data['meta']['code'] = 201
            response_data['meta']['msg'] = '登录失败'
        finally:
            return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')

def getPassPort(phone):
    try:
        passPort = PassPort.objects.get(phone=phone)
        return passPort
    except Exception, e:
        raise False

def webGetFundInfo(fundCode):
    try:
        html = 'http://fund.eastmoney.com/%s.html' % fundCode

        web = urllib2.urlopen(html)
        content = web.read()
        soup = BeautifulSoup(content,'html.parser')
        fundName = soup.title.string.split('(')[0]
        types = soup.find('div',class_='rightbottom').contents[0].find_all('td')[1].find('a').contents[0]
        fundInfo = {}

        fundInfo['fundName'] = fundName
        fundInfo['types'] = types

        return fundInfo
    except Exception, e:
        return False
    
def webGetFundNet(fundCode):
    try:
        html = 'http://fund.eastmoney.com/%s.html' % fundCode
        web = urllib2.urlopen(html)
        content = web.read()
        soup = BeautifulSoup(content,'html.parser')
        date = soup.find_all('li', class_='rq')
        net = soup.find_all('li', class_='dwjz')
        yields = soup.find_all('li', class_='zdf')

        fundNet = {}

        for i in range(1,len(date)):
            key = str(date[i].contents[0])
            value_net = net[i].contents[0].contents[0]
            value_yields = yields[i].contents[0].contents[0]
            value = '%s,%s' % (float(value_net), float(value_yields[:-1])*0.01)
            fundNet[key] = value
        return fundNet
    except Exception, e:
        return False
    

def getFund(fundCode):
    try:
        fund = Fund.objects.get(code=fundCode)
        return fund
    except Exception, e:
        return False

def getHighRiskFund(passPort):
    highRiskFundExist = UserFundShare.objects.filter(passPort=passPort,types='highRisk')
    return highRiskFundExist

def getMiddleRiskFund(passPort):
    highRiskFundExist = UserFundShare.objects.filter(passPort=passPort,types='middleRisk')
    return highRiskFundExist

def getLowRiskFund(passPort):
    highRiskFundExist = UserFundShare.objects.filter(passPort=passPort,types='lowRisk')
    return highRiskFundExist

def getThisYear():
    today = datetime.date.today()
    return today.year

def addFund(fundCode):
    try:
        fundInfo = webGetFundInfo(fundCode)
        if fundInfo:
            newFund = Fund(
                code = fundCode,
                name = fundInfo['fundName'],
                types = fundInfo['types'],

                cx3years = -1,
                cx5years = -1,   
                cxCode = ''
            )        
            newFund.save()
            return True
        else：
            return False
    except Exception, e:
        return False

def getFundNet(fund,day):
    try:
        fundNetExist = FundNet.objects.get(fund=fund,date=day)
        return fundNetExist
    except Exception, e:
        return False

def updateFundNet(fundCode):
    fund = getFund(fundCode)
    fundNet = webGetFundNet(fundCode)
    if fund and fundNet:
        n = 0
        for netInfo in fundNet:
            year = netInfo.split('-')[0]
            month = netInfo.split('-')[1]
            day = netInfo.split('-')[2]
            thatDay = datetime.date(year,month,day)
            if getFundNet(fund,thatDay):
                pass
            else：               
                newFundNet = FundNet(
                    fund = fund,
                    date = thatDay,
                    net = fundNet(netInfo).split(',')[0],
                    yields = fundNet(netInfo).split(',')[1]
                )
                newFundNet.save()
                n += 1
        today = datetime.date.today()
        if today.isoformat() in fundNet:
            return '%sdays,today' % n
        else：
            return '%sdays,noToday' % n
    else：
        return False

def addShare(passPort,fund,types,share):
    try:
        shareExist = UserFundShare.objects.get(passPort=passPort,fund=fund)
        if shareExist.share > 0.0:
            return False
        else:
            shareExist.share = share
            shareExist.types = types
            shareExist.save()
            return True

    except Exception, e:
        try:
            newShare = UserFundShare(
                passPort = passPort,
                fund = fund,
                types = types,
                share = share
            )
            newShare.save()
            return True
        except Exception, e:
            return False

def getShare(passPort,fund):
    try:
        shareExist = UserFundShare.objects.get(passPort=passPort,fund=fund)
        if shareExist.share > 0.0:
            return True
        else:
            return False
    except Exception, e:
        return False 

def addOldProfit(passPort,fund,year,profitBefore):
    profit = float(profitBefore)
    try:
        oldProfitExist = UserFundOldProfit.objects.get(passPort=passPort,fund=fund,year=year)
        oldProfitExist.profit = profit
        oldProfitExist.save()
        return True
    except Exception, e:
        try:
            newOldProfit = UserFundOldProfit(
                passPort = passPort,
                fund = fund,
                year = year,
                profit = profit
            )
            newOldProfit.save()
            return True
        except Exception, e:
            return False
        

def userAddFund(request):
    if 'phone' in request.POST and 'fundCode' in request.POST and 'share' in request.POST and
        'profitBefore' in request.POST and 'types' in request.POST:
        phone = request.POST.get('phone') 

        response_data = {
            "meta":{
                "code":200,
                "msg":''
            },
            "data":""
        }

        #手机号存在
        if getPassPort(phone):
            passPort = getPassPort(phone)
            
            fundCode = request.POST.get('fundCode')
            types = request.POST.get('types')
            share = request.POST.get('share')
            profitBefore = request.POST.get('profitBefore')
            year = getThisYear()

            #基金已收录
            if getFund(fundCode):
                fund = getFund(fundCode)
                # 份额已存在
                if getShare(passPort,fund):
                    response_data['meta']['code'] = 201
                    response_data['meta']['msg'] = '基金已收录，份额已存在，添加失败'

                    return HttpResponse(json.dumps(response_data), 
                        content_type='application/json')
                #份额不存在
                else:
                    try:                      
                        if addShare(passPort,fund,types,share):
                            pass
                        else：
                            response_data['meta']['code'] = 202
                            response_data['meta']['msg'] = '基金已收录，添加份额失败'
                            return HttpResponse(json.dumps(response_data), 
                                content_type='application/json')

                        if addOldProfit(passPort,fund,year,profitBefore):
                            response_data['meta']['code'] = 200
                            response_data['meta']['msg'] = '基金已收录，添加成功'
                            updateFundNet(fundCode)
                        else：
                            justAdd = getShare(passPort,fund)
                            justAdd.delete()
                            response_data['meta']['code'] = 203
                            response_data['meta']['msg'] = '基金已收录，添加份额成功，添加今年收益失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')
                        
                    except Exception, e:
                        response_data['meta']['code'] = 204
                        response_data['meta']['msg'] = '基金已收录，未知原因失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')                        
                
            #基金未收录
            else：             
                #收录基金成功
                if addFund(fundCode): 
                    fund = getFund(fundCode)
                    try:
                        if addShare(passPort,fund,types,share):
                            pass
                        else：
                            response_data['meta']['code'] = 205
                            response_data['meta']['msg'] = '收录基金成功，添加份额失败'
                            return HttpResponse(json.dumps(response_data), 
                                content_type='application/json')

                        if addOldProfit(passPort,fund,year,profitBefore):                   
                            response_data['meta']['code'] = 200
                            response_data['meta']['msg'] = '收录基金成功，添加成功'
                            updateFundNet(fundCode)
                        else：
                            justAdd = getShare(passPort,fund)
                            justAdd.delete()
                            response_data['meta']['code'] = 206
                            response_data['meta']['msg'] = '收录基金成功，添加份额成功，添加今年收益失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')
                    except Exception, e:
                        response_data['meta']['code'] = 207
                        response_data['meta']['msg'] = '收录基金成功，未知原因失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')  
                #收录基金失败
                else：
                    response_data['meta']['code'] = 208
                    response_data['meta']['msg'] = '收录基金失败'
                    return HttpResponse(json.dumps(response_data), 
                        content_type='application/json')

        #手机号不存在
        else：
            response_data['meta']['code'] = 209
            response_data['meta']['msg'] = '账号不存在'
            return HttpResponse(json.dumps(response_data), 
                content_type='application/json')
