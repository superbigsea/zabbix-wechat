#!/usr/local/bin/python3.5
# coding: utf-8
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zabbixwechat.common import *
from zabbix_wechat_db.models import ALARM_INFO


@csrf_exempt
def singlecomfirm(request):
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
        text = "确认状态：已确认 \n确认人：{0} \n{1} \n报警id：{2}".format(
            nickname, alarm_title, ID)
        senddata(text,toparty,toagent)
        respone = "确认成功"
    else:
        NICK_NAME = DATA.CONFIRM_USER_ID
        respone = "该告警已经被用户{0}确认过了".format(NICK_NAME)
    return HttpResponse(respone)
