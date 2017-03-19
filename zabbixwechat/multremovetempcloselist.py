#!/usr/local/bin/python3.5
import json
import time
from zabbixwechat.common import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from zabbix_wechat_db.models import TEMP_CLOSED


@csrf_exempt
def multremovetempcloselist(request):
    if(len(request.POST)) == 1:
        respone = "请勾条目"
    else:
        text = ""
        username = request.POST['username']
        nickname = findnickname(username)
        for ID in request.POST:
            if ID != 'username':
                TEMP_CLOSED.objects.filter(
                    id=ID).update(
                    REMOVED="ads")

                print(ID)
        respone = "批量删成功"
    return HttpResponse(respone)
