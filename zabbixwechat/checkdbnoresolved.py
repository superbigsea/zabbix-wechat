# coding: utf-8
from zabbixwechat.common import *
from django.shortcuts import render
from zabbix_wechat_db.models import ALARM_INFO
import os
import time


def checkdbnoresolved():
    callgettext()
    now = int(time.time())
    hosts= ALARM_INFO.objects.filter(
        CONFIRM_TIME="",
        RESOLVE_TIME="",
        SEVERITY__gt=1,
        ALARM_TIME__gt=now -
        86400,
        ALARM_TIME__lt=now -
        600).values_list('HOST_GROUP').distinct()
    if len(hosts)!=0:
        for i in hosts:
            num = ALARM_INFO.objects.filter(
                CONFIRM_TIME="",
                RESOLVE_TIME="",
                SEVERITY__gt=1,
                HOST_GROUP=i[0],
                ALARM_TIME__gt=now - 86400,
                ALARM_TIME__lt=now -600).count()
            data = _("There are {0} alarms in regin {1}  has not been comfirmed").format(num,i[0])
            agentid=findagentid(i[0]) 
            content = [{"title": "{0}".format(data)}]
            toparty = findgroupid(i[0])
            senddatanews(content,toparty,agentid)
    print ("OK")
