#!/usr/local/bin/python3.5
import json
import time
from zabbixwechat.common import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from zabbix_wechat_db.models import ALARM_INFO


@csrf_exempt
def multcomfirm(request):
    callgettext()
    if len(request.GET)==1:
        respone = "Please check the alarm entry"
    else:
        text = ""
        duplicate = ""
        idlist=[]
        username = request.GET['username']
        agentid = request.GET['agentid']
        nickname = findnickname(username)
        for ID in request.GET:
            if ID != 'username' and ID != 'winzoom' and ID != 'agentid':
                if ALARM_INFO.objects.filter(id=ID)[0].CONFIRM_TIME=='':
                    CONFIRM_TIME = int(time.time())
                    CONFIRM_PERIOD = CONFIRM_TIME - \
                        int(ALARM_INFO.objects.filter(id=ID)[0].ALARM_TIME)
                    ALARM_INFO.objects.filter(
                        id=ID).update(
                        CONFIRM_TIME=CONFIRM_TIME,
                        CONFIRM_PERIOD=CONFIRM_PERIOD,
                        CONFIRM_USER_ID=nickname)
                    text = str(ID) + ',' + text
                    idlist.append(ID)
        if text!="":         
            grouplist=ALARM_INFO.objects.filter(id__in=idlist).values_list('HOST_GROUP', flat=True).distinct()
            for i in grouplist:
                idlist2=""
                for j in idlist:
                    if ALARM_INFO.objects.filter(id=j)[0].HOST_GROUP==i:
                        idlist2= str(j) + ',' + idlist2         
                text = _("In region {0},{1} the above alarms have been confirmed by {2}").format(i,idlist2,nickname)
                toparty=findgroupid(i)
                senddata(text,toparty,agentid)
            respone = _("Operate successfully")
        else :
            respone =_("This alame has been confirmed before")
    return HttpResponse(respone)

