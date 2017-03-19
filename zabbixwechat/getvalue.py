#!/usr/local/bin/python3.5
import pymysql
import sys
import json
import time
from zabbixwechat.common import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from zabbix_wechat_db.models import ALARM_INFO
from zabbix_wechat_db.models import TEMP_CLOSED
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random
import configparser
from urllib import parse

cf = configparser.ConfigParser()
cf.read("/etc/zabbix/wechat.conf")

logging.basicConfig(
    filename='/var/log/zabbix/wechat.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

with open('/etc/zabbix/pri.key') as f:
    key = f.read()


@csrf_exempt
def getvalue(request):
    random_generator = Random.new().read
    cipher_text=request.POST['data']
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
    data=eval(text.decode())
    ALARM_ID = data['eventid']
    ALARM_TITLE = data['alarm_title']
    ALARM_STATUS = data['alarm_status']
    ALARM_STATUS_EN = data['alarm_status']
    HOST_NAME = data['host_name']
    HOSTCONN = data['hostconn']
    TRIGGERDESCRIPTION = data['triggerdescription']
    HOST_GROUP = data['host_group']
    count = 0
    while (HOST_GROUP.split(',')[count]=="Discovered hosts"):
            count+=1
    HOST_GROUP=HOST_GROUP.split(',')[count]

    TRIGGERSEVERITY = data['triggerseverity']
    ALARM_TIME = int(time.time())
    DUTY_ROSTER = getdutyroster()
    if TRIGGERSEVERITY == "Disaster":
        SEVERITY = 5
        SEVERITY_CHS = "灾难"
    elif TRIGGERSEVERITY == "High":
        SEVERITY = 4
        SEVERITY_CHS = "严重"
    elif TRIGGERSEVERITY == "Average":
        SEVERITY = 3
        SEVERITY_CHS = "一般严重"
    elif TRIGGERSEVERITY == "Warning":
        SEVERITY = 2
        SEVERITY_CHS = "警告"
    elif TRIGGERSEVERITY == "Information":
        SEVERITY = 1
        SEVERITY_CHS = "通知"
    else:
        SEVERITY = 0
        SEVERITY_CHS = "未定义"
    if ALARM_STATUS == "OK":
        ALARM_STATUS = "已解除"
    elif ALARM_STATUS == "PROBLEM":
        ALARM_STATUS = "已触发"
    else:
        ALARM_STATUS = "报警状态未知"
    ONEDAYTIMES = ALARM_INFO.objects.filter(
        HOST_NAME=HOST_NAME,
        ALARM_TITLE=ALARM_TITLE,
        ALARM_TIME__gt=int(
            time.time()) - 86400,
        HOST_GROUP=HOST_GROUP).count()
    ONEWEEKTIMES = ALARM_INFO.objects.filter(
        HOST_NAME=HOST_NAME,
        ALARM_TITLE=ALARM_TITLE,
        ALARM_TIME__gt=int(
            time.time()) - 604800,
        HOST_GROUP=HOST_GROUP).count()
    if ALARM_STATUS == "已触发" and  TEMP_CLOSED.objects.filter(HOST_NAME=HOST_NAME,HOST_GROUP=HOST_GROUP,ALARM_TITLE=ALARM_TITLE,REMOVED='',ENDTIME__gt=int(
            time.time())).count()==0:
        ID = ALARM_INFO.objects.create(
            ALARM_ID=ALARM_ID,
            ALARM_TITLE=ALARM_TITLE,
            ALARM_TIME=ALARM_TIME,
            MESSAGE=TRIGGERDESCRIPTION,
            HOST_NAME=HOST_NAME,
            SEVERITY=SEVERITY,
            HOST_GROUP=HOST_GROUP).id
    if ALARM_STATUS == "已解除"  and TEMP_CLOSED.objects.filter(HOST_NAME=HOST_NAME,HOST_GROUP=HOST_GROUP,ALARM_TITLE=ALARM_TITLE,REMOVED='',ENDTIME__gt=int(
            time.time())).count()==0:
        DATA = ALARM_INFO.objects.filter(
            HOST_GROUP=HOST_GROUP, ALARM_ID=ALARM_ID)
        RESOLVE_PERIOD = int(time.time()) - int(DATA[0].ALARM_TIME)
        ID = DATA[0].id
        DATA.update(
            RESOLVE_TIME=int(
                time.time()),
            RESOLVE_PERIOD=RESOLVE_PERIOD)
    senddata(
            ALARM_TITLE,
            ALARM_STATUS,
            (str(
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    (time.localtime(ALARM_TIME))))),
            HOST_NAME,
            HOSTCONN,
            TRIGGERDESCRIPTION,
            ALARM_ID,
            SEVERITY_CHS,
            ONEDAYTIMES,
            ONEWEEKTIMES,
            HOST_GROUP,
            DUTY_ROSTER,
            ID,SEVERITY)
    if ALARM_STATUS == "已触发":
        return HttpResponse(ID)
    if ALARM_STATUS == "已解除":
        return HttpResponse("已解除:{0}".format(ID))


def senddata(
        ALARM_TITLE,
        ALARM_STATUS,
        TIME,
        HOST_NAME,
        HOSTCONN,
        MESSAGE,
        ALARM_ID,
        SEVERITY_CHS,
        ONEDAYTIMES,
        ONEWEEKTIMES,
        HOST_GROUP,
        DUTY_ROSTER,
        ID,SEVERITY):
    url=cf.get("wechat", "url")
    url_encode=parse.quote_plus(url)
    imageurl = "{1}:1978/{0}.png".format(ID,url)
    comfirmurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri={1}singlecomfirm&response_type=code&scope=snsapi_base&state={0}&connect_redirect=1#wechat_redirect".format(
        ID,url_encode)
    detailurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri={1}detail&response_type=code&scope=snsapi_base&state={0}#wechat_redirect".format(
        ID,url_encode)
    tempcloseurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri={1}tempclosealarm&response_type=code&scope=snsapi_base&state={0}&connect_redirect=1#wechat_redirect".format(
        ID,url_encode)
    send_values = [
        {
            "url": "{0}".format(detailurl),
            "title": "{0} {1}".format(ALARM_STATUS,ALARM_TITLE),
        },
        {
            "title": "报警主机:{1}({2})\n时间:{3}".format(ALARM_STATUS, HOST_NAME, HOSTCONN, TIME),
        },
        {
            "title": "区域：{0}\nID:{2}".format(HOST_GROUP, SEVERITY_CHS, ID),"picurl": "{0}".format(serverityimageurl),
        },
        {
            "title": "运维值班人员:{0}".format(DUTY_ROSTER),
        },

    ]
    
    if ALARM_STATUS == "已触发":
        text = {"title": "确认报警", "url": "{0}".format(comfirmurl), }
        send_values.append(text)
    if  len(MESSAGE)!=0: 
        text = {"title": "报警说明:{0}".format(MESSAGE), }
        send_values.insert(3, text)
    if ONEDAYTIMES > 3 or ONEWEEKTIMES > 7:
        text = {
            "title": "该报警一天内发生{0}次，一周内发送{1}次,点击本行临时关闭该主机的该报警12小时".format(
                ONEDAYTIMES, ONEWEEKTIMES),"url": "{0}".format(tempcloseurl),  }
        send_values.append(text)
    send_values[0].update( {"picurl": "{0}".format(imageurl)})
    toparty = cf.get("wechat", "toparty")
    toagent = cf.get("wechat", "agentid")
    senddatanews(send_values,toparty,toagent)
