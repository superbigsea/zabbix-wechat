from django.http import HttpResponse
from zabbixwechat.common import *
from django.shortcuts import render
from zabbix_wechat_db.models import ALARM_INFO
import time


def tempcloselist(request):
    now = int(time.time())
    code = request.GET['code']
    state = request.GET['state']
    comfirmuser = getusername(code)
    context = {}
    list = TEMP_CLOSED.objects.filter(
        # ENDTIME__gt=now,REMOVED=1).order_by("-id")
        REMOVED='', ENDTIME__gt=now).order_by("-id")
    for i in list:
        i.BEGINTIME = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(i.BEGINTIME)))
        i.ENDTIME = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(i.ENDTIME)))
    context['body'] = list
    context['username'] = comfirmuser
    return render(request, 'tempcloselist.html', context)
