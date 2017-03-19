#!/usr/local/bin/python3.5
from zabbixwechat.common import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zabbix_wechat_db.models import ALARM_INFO


@csrf_exempt
def report(request):
    message = request.POST['message']
    comfirmuser = request.POST['comfirmuser']
    ID = request.POST['id']
    username = findnickname(comfirmuser)
    DATA = ALARM_INFO.objects.filter(id=ID)[0]
    ALARM_TITLE = DATA.ALARM_TITLE
    ALARM_TIME = time.strftime("%Y-%m-%d %H:%M:%S",
                               (time.localtime(int(DATA.ALARM_TIME))))
    message = "报警 ID:{0}\n报警标题：{3}\n报警触发时间:{4}\n汇报人：{1}\n汇报内容：{2}".format(
        ID, username, message, ALARM_TITLE, ALARM_TIME)
    senddata(message)
    return HttpResponse("汇报报警成功")
