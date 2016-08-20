#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('the433.views',
    url(r'^passport/register/$', 'register', name='register'),
    url(r'^passport/login/$', 'login', name='login'),
    url(r'^fund/useraddfund/$', 'userAddFund', name='userAddFund'),
    url(r'^fund/deletefund/$', 'deleteFund', name='deleteFund'),
    url(r'^homepage/gethighrisk/$', 'HPgetHighRisk', name='HPgetHighRisk'),
    url(r'^homepage/getmiddlerisk/$', 'HPgetMiddleRisk', name='HPgetMiddleRisk'),
    url(r'^homepage/getlowrisk/$', 'HPgetLowRisk', name='HPgetLowRisk'),
    url(r'^homepage/maininfo/$', 'HPgetMainInfo', name='HPgetMainInfo'),
    url(r'^funddetali/editshare/$', 'editShare', name='editShare'),
    url(r'^passport/editnicname/$', 'editNicName', name='editNicName'),
    url(r'^version/update/$', 'versionUpdate', name='versionUpdate'),
    url(r'^repair/UserDayFundProfit/(?P<fromDay>d{8})/(?P<toDay>d{8})/$', 'repairUserDayFundProfit', name='repairUserDayFundProfit'),
    url(r'^test/$', 'test', name='test'),

)