#!/usr/local/python3.51/bin/python3.5
# coding: utf-8
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from zabbixwechat.common import *
from zabbix_wechat_db.models import ALARM_INFO


@csrf_exempt
def detail(request):
    code = request.GET['code']
    username = getusername(code)
    state = request.GET['state']
    ID = state
    DATA = ALARM_INFO.objects.filter(id=ID)[0]
    context = {}
    context['ID'] = DATA.id
    context['ALARM_TITLE'] = DATA.ALARM_TITLE
    context['HOST_GROUP'] = DATA.HOST_GROUP
    context['ALARM_TIME'] = time.strftime(
        "%Y-%m-%d %H:%M:%S", (time.localtime(int(DATA.ALARM_TIME))))
    context['username'] = username
    return render(request, 'detail.html', context)
