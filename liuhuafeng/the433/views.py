#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from the433.models import PassPort,Profile,Fund,FundNet,UserFundShare,UserFundProfit,UserFundOldProfit,UserDayProfit
from bs4 import BeautifulSoup
import urllib2
from django.views.decorators.csrf import csrf_exempt

#获取昨天date
def getYesterday(date):
    yesterday = date - datetime.timedelta(days=1)
    return yesterday

@csrf_exempt
def register(request):
    if request.method == 'POST':
    	#data=simplejson.loads(request.raw_post_data)
        response_data = {
            "meta":{
                "code":0,
                "msg":''
            },
            "data":""
        }

    	if 'phone' in request.POST and 'pwd' in request.POST and 'nicName' in request.POST:
    		
            try:
                phone = str(request.POST.get('phone'))
                pwd = str(request.POST.get('pwd'))
                nicName = str(request.POST.get('nicName'))
            except Exception, e:
                response_data['meta']['code'] = 203
                response_data['meta']['msg'] = '参数格式有误'
                return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')


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
                response_data['meta']['code'] = 200
                response_data['meta']['msg'] = '注册成功'
            finally:
                return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')

        else:
            response_data['meta']['code'] = 202
            response_data['meta']['msg'] = '参数有误'
    	    return HttpResponse(json.dumps(response_data), 
                content_type='application/json')
    else:
        response_data = {
            "meta":{
                "code": 204,
                "msg": '访问方式有误'
            },
            "data":""
        }
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

@csrf_exempt
def login(request):
    if 'phone' in request.POST and 'pwd' in request.POST:
        response_data = {
            "meta":{
                "code":0,
                "msg":''
            },
            "data":""
        }
        try:
            phone = request.POST.get('phone')
            pwd = request.POST.get('pwd')
            passPortExist = PassPort.objects.get(phone=phone,pwd=pwd)
            response_data['meta']['code'] = 200
            response_data['meta']['msg'] = '登录成功'
        except Exception, e:
            response_data['meta']['code'] = 201
            response_data['meta']['msg'] = '登录失败'
        finally:
            return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')
    else:
        response_data = {
            "meta":{
                "code": 202,
                "msg": u'访问方式有误'
            },
            "data":""
        }
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

#利用手机号获取通行证，成功则返回通行证，失败则返回False
def phoneGetPassPort(phone):
    try:
        passPort = PassPort.objects.get(phone=phone)
        return passPort
    except Exception, e:
        raise False

#抓取基金信息，成功则返回字典，失败则返回False
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

#抓取基金净值，成功则返回字典，失败则返回False
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
    
#利用基金代码获取基金，若不存在则返回False，成功则返回Fund
def getFund(fundCode):
    try:
        fund = Fund.objects.get(code=fundCode)
        return fund
    except Exception, e:
        return False

#获取今年年份int
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
        else:
            return False
    except Exception, e:
        return False

#获取某日基金净值，存在则返回FundNet，否则返回False
def getFundNet(fund,date):
    try:
        fundNetExist = FundNet.objects.get(fund=fund,date=date)
        return fundNetExist
    except Exception, e:
        return False

#更新基金净值，更新失败则返回False，成功则返回字符串，包含更新天数和今天是否在内
def updateFundNet(fundCode):
    fund = getFund(fundCode)
    fundNet = webGetFundNet(fundCode)

    if fund and fundNet:
        n = 0
        for netInfo in fundNet:
            year = int(netInfo.split('-')[0])
            month = int(netInfo.split('-')[1])
            day = int(netInfo.split('-')[2])
            thatDay = datetime.date(year,month,day)
            try:
                fundNetExist = FundNet.objects.get(fund=fund,date=thatDay)
                pass
            except Exception, e:               
                newFundNet = FundNet(
                    fund = fund,
                    date = thatDay,
                    net = fundNet[netInfo].split(',')[0],
                    yields = fundNet[netInfo].split(',')[1]
                )
                newFundNet.save()
                n += 1
        today = datetime.date.today()
        if today.isoformat() in fundNet:
            return '%sdays,today' % n
        else:
            return '%sdays,noToday' % n
    else:
        return False

#增加份额，添加成功则返回True，否则返回False
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

#获取基金份额，份额存在且大于0.0则返回True
def getShare(passPort,fund):
    try:
        shareExist = UserFundShare.objects.get(passPort=passPort,fund=fund)
        if shareExist.share > 0.0:
            return True
        else:
            return False
    except Exception, e:
        return False 

#添加某基金今年历史收益，成功则返回True，否则返回False
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

#用户添加基金        
@csrf_exempt
def userAddFund(request):
    if 'phone' in request.POST and 'fundCode' in request.POST and 'share' in request.POST and 'profitBefore' in request.POST and 'types' in request.POST:
        phone = request.POST.get('phone') 

        response_data = {
            "meta":{
                "code":201,
                "msg":''
            },
            "data":""
        }

        #手机号存在
        if phoneGetPassPort(phone):
            passPort = phoneGetPassPort(phone)
            
            fundCode = request.POST.get('fundCode')
            types = request.POST.get('types')
            if types in ['lowRisk','middleRisk','highRisk']:
                pass
            else:
                response_data['meta']['msg'] = '风险类型有误'
                return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')
            try:
                share = float(request.POST.get('share'))
                profitBefore = float(request.POST.get('profitBefore'))
            except Exception, e:
                response_data['meta']['msg'] = '收益或份额格式有误'
                return HttpResponse(json.dumps(response_data), 
                    content_type='application/json')
            
            year = getThisYear()

            #基金已收录
            if getFund(fundCode):
                fund = getFund(fundCode)
                # 份额已存在
                if getShare(passPort,fund):
                    response_data['meta']['msg'] = '基金已收录，份额已存在，添加失败'

                    return HttpResponse(json.dumps(response_data), 
                        content_type='application/json')
                #份额不存在
                else:
                    try:                      
                        if addShare(passPort,fund,types,share):
                            pass
                        else:
                            response_data['meta']['msg'] = '基金已收录，添加份额失败'
                            return HttpResponse(json.dumps(response_data), 
                                content_type='application/json')

                        if addOldProfit(passPort,fund,year,profitBefore):
                            response_data['meta']['code'] = 200
                            response_data['meta']['msg'] = '基金已收录，添加成功'
                            updateFundNet(fundCode)
                        else:
                            justAdd = getShare(passPort,fund)
                            justAdd.delete()
                            response_data['meta']['msg'] = '基金已收录，添加份额成功，添加今年收益失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')
                        
                    except Exception, e:
                        response_data['meta']['msg'] = '基金已收录，未知原因失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')                        
                
            #基金未收录
            else:             
                #收录基金成功
                if addFund(fundCode): 
                    fund = getFund(fundCode)
                    try:
                        if addShare(passPort,fund,types,share):
                            pass
                        else:
                            response_data['meta']['msg'] = '收录基金成功，添加份额失败'
                            return HttpResponse(json.dumps(response_data), 
                                content_type='application/json')

                        if addOldProfit(passPort,fund,year,profitBefore):                   
                            response_data['meta']['code'] = 200
                            response_data['meta']['msg'] = '收录基金成功，添加成功'
                            updateFundNet(fundCode)
                        else:
                            justAdd = getShare(passPort,fund)
                            justAdd.delete()
                            response_data['meta']['msg'] = '收录基金成功，添加份额成功，添加今年收益失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')
                    except Exception, e:
                        response_data['meta']['msg'] = '收录基金成功，未知原因失败'
                        return HttpResponse(json.dumps(response_data), 
                            content_type='application/json')  
                #收录基金失败
                else:
                    response_data['meta']['msg'] = '收录基金失败'
                    return HttpResponse(json.dumps(response_data), 
                        content_type='application/json')

        #手机号不存在
        else:
            response_data['meta']['msg'] = '账号不存在'
            return HttpResponse(json.dumps(response_data), 
                content_type='application/json')
    else:
        response_data = {
            "meta":{
                "code":201,
                "msg":'参数有误'
            },
            "data":""
        }        
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

#获取前一日基金净值，返回前一日FundNet或False
def getBeforeDayFundNet(fund, date):
    beforeDay = getYesterday(date)

    if getFundNet(fund,beforeDay):
        return getFundNet(fund,beforeDay)
    else:
        for delta in xrange(1,20):
            beforeDay = getYesterday(beforeDay)
            if getFundNet(fund,beforeDay):
                return getFundNet(fund,beforeDay)
        return False

#更新用户每个基金每日收益，更新成功返回True，否则返回False
def updateUserFundProfit(passPort,date,fund):
    try:
        userFundProfitExist = UserFundProfit.objects.get(passPort=passPort,date=date,fund=fund)
        #print u'%s已经存在' % fund.name
        return False
    except Exception, e:
        #print 1
        todayFNet = getFundNet(fund,date)
        yesterdayFNet = getBeforeDayFundNet(fund, date)
        #print 2
        if todayFNet and yesterdayFNet:
            userFundShare = UserFundShare.objects.get(passPort=passPort,fund=fund)
            #print 3
            share = userFundShare.share
            #print share
            profit = (todayFNet.net - yesterdayFNet.net) * share
            #print 4
            totalAmount = yesterdayFNet.net * share

            newUserFundProfit = UserFundProfit(
                passPort = passPort,
                fund = fund,
                date = date,
                todayNet = todayFNet.net,
                beforeDayNet = yesterdayFNet.net,
                share = share,
                yields = todayFNet.yields,
                profit = float("%.2f" % profit),
                totalAmount = float("%.2f" % totalAmount)
                )
            newUserFundProfit.save()
            return True
        else:
            return False

#获取用户当日基金的总收益和总资金，若存在没有今日收益的基金或更新失败则返回False
def getUserFundDayProfit(passPort,date):
    userFunds = UserFundShare.objects.filter(passPort=passPort,share__gt=0.0)
    if userFunds:
        funds = []
        fundsProfit = []
        for fundShare in userFunds:
            funds.append(fundShare.fund)
        for fund in funds:
            try:
                UserFundProfitExist = UserFundProfit.objects.get(passPort=passPort,fund=fund,date=date)
                fundsProfit.append(UserFundProfitExist)
            except Exception, e:
                pass
        if len(funds) == len(fundsProfit):
            profit = 0.00
            totalAmount = 0.00
            for fundProfit in fundsProfit:
                profit += fundProfit.profit
                totalAmount += fundProfit.totalAmount
            result = []
            result.append(profit)
            result.append(totalAmount)
            return result
        else:
            return False
    else:
        return False

#更新用户当日总收益（当前仅包含基金），若更新失败则返回False，成功则返回True
def updateUserProfit(passPort,date):
    try:
        userDayProfitExist = UserDayProfit.objects.get(passPort=passPort,date=date)
        return False
    except Exception, e:
        fundData = getUserFundDayProfit(passPort,date)
        if fundData:
            profit = fundData[0]
            totalAmount = fundData[1]
            yields = profit / totalAmount

            newUserDayProfit = UserDayProfit(
                passPort = passPort,
                date = date,
                profit = profit,
                totalAmount = totalAmount,
                yields = yields
                )
            newUserDayProfit.save()
            return True
        else:
            return False

#获取用户某基金的历史总收益
def getFundTotalProfit(passPort,fund):
    profit = 0.00

    fundProfits = UserFundProfit.objects.filter(passPort=passPort,fund=fund)
    #如果存在基金收益记录
    if fundProfits:       
        for fundProfit in fundProfits:
            profit += fundProfit.profit
        
    yearProfits = UserFundOldProfit.objects.filter(passPort=passPort,fund=fund)
    #如果存在基金往期收益记录
    if yearProfits:
        for yearProfit in yearProfits:
            profit += yearProfit.profit

    return profit

#获取用户资产信息的子函数
def tempAddInfo(temp,fundNet,fund,date,fundShare):
    net = fundNet.net
    yields = fundNet.yields
    beforeFundNet = getBeforeDayFundNet(fund,date)
    profit = (fundNet.net - beforeFundNet.net) * fundShare.share
    profit = float("%.2f" % profit)
    dayString = fundNet.date.isoformat()
    totalAmount = float("%.2f" % (net*fundShare.share))
    totalProfit = getFundTotalProfit(passPort,fund)

    temp.append(totalAmount)
    temp.append(totalProfit)
    temp.append(profit)
    temp.append(dayString)
    temp.append(fund.types)

    return temp

#获取用户某一类风险资产信息
def getRiskTypeInfo(phone,types):
    try:
        passPort = phoneGetPassPort(phone)
    except Exception, e:
        return 'passPort notfound'
    try:  
        userFundShares =  UserFundShare.objects.filter(passPort=passPort,types=types)
        today = datetime.date.today()
        
        #如果用户份额FundShare存在
        if userFundShares:
            result = []

            #对于每一个用户份额FundShare，收集基金的名字、代码、总资产、总收益、最新收益、最新收益率、最新收益时间
            for fundShare in userFundShares:
                temp = {}
                fund = fundShare.fund

                #收集基金名字和代码
                temp['name'] = str(fund.name)
                temp['code'] = str(fund.code)

                #获取最新的FundNet
                latestFundNet = FundNet.objects.filter(fund=fund).latest('date')
                net = latestFundNet.net
                #yields = latestFundNet.yields
                totalAmount = float("%.2f" % (net*fundShare.share))
                totalProfit = getFundTotalProfit(passPort,fund)

                #收集基金总资金和总收益
                temp['totalAmount'] = str(totalAmount)
                temp['totalProfit'] = str(totalProfit)

                #如果有用户基金收益记录
                try:
                    latestFundProfit = UserFundProfit.objects.filter(passPort=passPort,fund=fund).latest('date')
                    latestProfit = latestFundProfit.profit
                    latestYields = latestFundProfit.yields
                    dayString = latestFundProfit.date.isoformat()

                    #收集基金最新收益、最新收益率、最新日期
                    temp['latestProfit'] = str(latestProfit)
                    temp['latestYields'] = str(latestYields)
                    temp['dayString'] = str(dayString)
                    temp['net'] = str(net)
                    temp['share'] = str(fundShare.share)

                #没有基金收益记录，可能是新添加的基金
                except Exception, e:

                    #收集基金最新收益、最新收益率、最新日期
                    temp['latestProfit'] = ''
                    temp['latestYields'] = ''
                    temp['dayString'] = ''
                    temp['net'] = ''
                    temp['share'] = ''
                
                #收集基金分类
                temp['types'] = str(fund.types)                   

                result.append(temp)

            return result
        else:
            return 'no fundShare'

    except Exception, e:
        return 'something wrong'

#首页获取高风险资产信息
@csrf_exempt
def HPgetHighRisk(request):
    if 'phone' in request.POST:
        response_data = {
            "meta":{
                "code":0,
                "msg":''
            },
            "data":""
        }

        phone = request.POST.get('phone')

        result = getRiskTypeInfo(phone,'highRisk')
        if result:
            response_data['meta']['code'] = 200
            response_data['meta']['msg'] = u'获取成功'
            response_data['data'] = result
        else:
            response_data['meta']['code'] = 201
            response_data['meta']['msg'] = u'无信息或获取失败'
            response_data['data'] = result
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

    else:
        response_data = {
            "meta":{
                "code": 202,
                "msg": u'参数有误'
            },
            "data":""
        }
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

#首页获取中风险资产信息
@csrf_exempt
def HPgetMiddleRisk(request):
    if 'phone' in request.POST:
        response_data = {
            "meta":{
                "code":0,
                "msg":''
            },
            "data":""
        }

        phone = request.POST.get('phone')

        result = getRiskTypeInfo(phone,'middleRisk')
        if result:
            response_data['meta']['code'] = 200
            response_data['meta']['msg'] = u'获取成功'
            response_data['data'] = result
        else:
            response_data['meta']['code'] = 201
            response_data['meta']['msg'] = u'无信息或获取失败'
            response_data['data'] = result
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

    else:
        response_data = {
            "meta":{
                "code": 202,
                "msg": u'参数有误'
            },
            "data":""
        }
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

#首页获取低风险资产信息
@csrf_exempt
def HPgetLowRisk(request):
    if 'phone' in request.POST:
        response_data = {
            "meta":{
                "code":0,
                "msg":''
            },
            "data":""
        }

        phone = request.POST.get('phone')

        result = getRiskTypeInfo(phone,'lowRisk')
        if result:
            response_data['meta']['code'] = 200
            response_data['meta']['msg'] = u'获取成功'
            response_data['data'] = result
        else:
            response_data['meta']['code'] = 201
            response_data['meta']['msg'] = u'无信息或获取失败'
            response_data['data'] = result
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

    else:
        response_data = {
            "meta":{
                "code": 202,
                "msg": u'参数有误'
            },
            "data":""
        }
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

#获取用户的总资产
def getUserTotalProperty(passPort):
    pass

#获取用户的累计收益
def getUserTotalProfit(passPort):
    pass

#获取首页主信息，包括昨日收益、总资产、累计收益
@csrf_exempt
def HPgetMainInfo(request):
    if 'phone' in request.POST:
        response_data = {
            "meta":{
                "code":0,
                "msg":''
            },
            "data":""
        }

        phone = request.POST.get('phone')
        passPort = phoneGetPassPort(phone)

        totalProperty = getUserTotalProperty(passPort)
        totalProfit = getUserTotalProfit(passPort)

        #获取最新的日收益
        try:
            latestProfit = UserDayProfit.objects.filter(passPort=passPort).latest('date')
            profit = latestProfit.profit
            dayString = latestProfit.date.isoformat()
        #未获取到，可能是新用户
        except Exception, e:
            profit = ''
            dayString = ''
        
        response_data['meta']['code'] = 200
        response_data['meta']['msg'] = u'获取成功'
        
        response_data['data'] = {
            'totalProperty':str(totalProperty),
            'totalProfit':str(totalProfit),
            'profit':str(profit),
            'dayString':str(dayString)
            }

        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

        
    else:
        response_data = {
            "meta":{
                "code": 201,
                "msg": u'参数有误'
            },
            "data":""
        }
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')

def test(request):
    today = datetime.date.today()
    allUserFundShare = UserFundShare.objects.filter(share__gt=0.0)
    response_data = {
        "meta":{
            "code":000,
            "msg":''
        },
        "data":""
    }
    if allUserFundShare:
        for userFundShare in allUserFundShare:
            print u'现在计算用户%s的%s基金' % (userFundShare.passPort.phone,userFundShare.fund.name)

            result = updateUserFundProfit(userFundShare.passPort, today, userFundShare.fund)

            print result
        return HttpResponse(json.dumps(response_data), 
            content_type='application/json')
    else:
        pass
