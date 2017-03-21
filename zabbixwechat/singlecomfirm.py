#!/usr/local/bin/python3.5
# coding: utf-8
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zabbixwechat.common import *
from zabbix_wechat_db.models import ALARM_INFO


@csrf_exempt
def singlecomfirm(request):
    callgettext()
    code = request.GET['code']
    username = getusername(code)
    state = request.GET['state']
    ID = state
    comfirmtime = int(time.time())
    DATA = ALARM_INFO.objects.filter(id=ID)[0]
    if DATA.CONFIRM_TIME == "":
        eventtime = DATA.ALARM_TIME
        comfirmperiod = comfirmtime - int(eventtime)
        nickname = findnickname(username)
        alarm_title = DATA.ALARM_TITLE
        HOST_GROUP = DATA.HOST_GROUP
        toparty = findgroupid(HOST_GROUP)
        toagent = findagentid(HOST_GROUP)
        ALARM_INFO.objects.filter(
            id=ID).update(
            CONFIRM_TIME=comfirmtime,
            CONFIRM_PERIOD=comfirmperiod,
            CONFIRM_USER_ID=nickname)
        text = _("Alarm has been confirmed\nConfirm user :{0} \n{1} \nID：{2}").format(
            nickname, alarm_title, ID)
        senddata(text,toparty,toagent)
        respone = _("Operate successfully")
    else:
        respone = _("This alame has been confirmed before")
    return HttpResponse(respone)
