from django.http import HttpResponse
from zabbixwechat.common import *
from django.shortcuts import render
from zabbix_wechat_db.models import *
import time


def all(request):
    now = int(time.time())
    code = request.GET['code']
    state = request.GET['state']
    comfirmuser = getusername(code)
    context = {}
    if state == "1":
        list = ALARM_INFO.objects.filter(ALARM_TIME__gt=now - 86400).order_by("-id")
    if state == "2":
        list = ALARM_INFO.objects.filter(ALARM_TIME__gt=now - 86400,RESOLVE_TIME="",CONFIRM_TIME="").order_by("-id")
    if state == "3":
        list = ALARM_INFO.objects.filter(ALARM_TIME__gt=now - 86400,RESOLVE_TIME="").order_by("-id")
    for i in list:
        i.ALARM_TIME = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(i.ALARM_TIME)))
        if i.CONFIRM_TIME:
            i.CONFIRM_TIME = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(int(i.CONFIRM_TIME)))
        if i.RESOLVE_TIME:
            i.RESOLVE_TIME = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(int(i.RESOLVE_TIME)))
    context['body'] = list
    context['username'] = comfirmuser
    context['agentid'] = agentid
    return render(request, 'all.html', context)
