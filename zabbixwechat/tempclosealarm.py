#!/usr/local/bin/python3.5
# coding: utf-8
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zabbixwechat.common import *
from zabbix_wechat_db.models import ALARM_INFO
from zabbix_wechat_db.models import TEMP_CLOSED


@csrf_exempt
def tempclosealarm(request):
    code = request.GET['code']
    USER_ID = getusername(code)
    USER_ID = findnickname(USER_ID)
    state = request.GET['state']
    ID = state
    BEGINTIME = int(time.time())
    ENDTIME = int(time.time()) + 3600 * 12
    DATA = ALARM_INFO.objects.filter(id=ID)[0]
    HOST_NAME = DATA.HOST_NAME
    ALARM_TITLE = DATA.ALARM_TITLE
    HOST_GROUP = DATA.HOST_GROUP
    TEMP_CLOSED.objects.create(
        ALARM_TITLE=ALARM_TITLE,
        HOST_NAME=HOST_NAME,
        BEGINTIME=BEGINTIME,
        ENDTIME=ENDTIME,
        USER_ID=USER_ID,
        HOST_GROUP=HOST_GROUP)
    return HttpResponse("操作成功")
