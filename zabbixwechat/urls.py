"""zabbixwechat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from zabbixwechat.all import all
from zabbixwechat.multcomfirm import multcomfirm
from zabbixwechat.singlecomfirm import singlecomfirm
from zabbixwechat.getvalue import getvalue
from zabbixwechat.detail import detail
from zabbixwechat.report import report
from zabbixwechat.tempclosealarm import tempclosealarm
from zabbixwechat.tempcloselist import tempcloselist
from zabbixwechat.multremovetempcloselist import multremovetempcloselist
from zabbixwechat.checkdbnoresolved import checkdbnoresolved


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^alarm/all', all),
    url(r'^alarm/multcomfirm', multcomfirm),
    url(r'^alarm/singlecomfirm', singlecomfirm),
    url(r'^alarm/getvalue', getvalue),
    url(r'^alarm/detail', detail),
    url(r'^alarm/report', report),
    url(r'^alarm/checkdbnoresolved', checkdbnoresolved),
    url(r'^alarm/tempclosealarm', tempclosealarm),
    url(r'^alarm/tempcloselist', tempcloselist),
    url(r'^alarm/multremovetempcloselist', multremovetempcloselist),

]
