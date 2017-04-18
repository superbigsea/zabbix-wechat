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
    callgettext()
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
    elif TRIGGERSEVERITY == "High":
        SEVERITY = 4
    elif TRIGGERSEVERITY == "Average":
        SEVERITY = 3
    elif TRIGGERSEVERITY == "Warning":
        SEVERITY = 2
    elif TRIGGERSEVERITY == "Information":
        SEVERITY = 1
    else:
        SEVERITY = 0
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
    if ALARM_STATUS == "PROBLEM" and  TEMP_CLOSED.objects.filter(HOST_NAME=HOST_NAME,HOST_GROUP=HOST_GROUP,ALARM_TITLE=ALARM_TITLE,REMOVED='',ENDTIME__gt=int(
            time.time())).count()==0:
        ID = ALARM_INFO.objects.create(
            ALARM_ID=ALARM_ID,
            ALARM_TITLE=ALARM_TITLE,
            ALARM_TIME=ALARM_TIME,
            MESSAGE=TRIGGERDESCRIPTION,
            HOST_NAME=HOST_NAME,
            SEVERITY=SEVERITY,
            HOST_GROUP=HOST_GROUP).id
    if ALARM_STATUS == "OK"  and TEMP_CLOSED.objects.filter(HOST_NAME=HOST_NAME,HOST_GROUP=HOST_GROUP,ALARM_TITLE=ALARM_TITLE,REMOVED='',ENDTIME__gt=int(
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
            TRIGGERSEVERITY,
            ONEDAYTIMES,
            ONEWEEKTIMES,
            HOST_GROUP,
            DUTY_ROSTER,
            ID,SEVERITY)
    if ALARM_STATUS == "PROBLEM":
        return HttpResponse(ID)
    if ALARM_STATUS == "OK":
        return HttpResponse("OK:{0}".format(ID))


def senddata(
        ALARM_TITLE,
        ALARM_STATUS,
        TIME,
        HOST_NAME,
        HOSTCONN,
        MESSAGE,
        ALARM_ID,
        TRIGGERSEVERITY,
        ONEDAYTIMES,
        ONEWEEKTIMES,
        HOST_GROUP,
        DUTY_ROSTER,
        ID,SEVERITY):
    url=cf.get("wechat", "url")
    url_encode=parse.quote_plus(url)
    imageurl = "http://{1}/{0}.png".format(ID,url)
    comfirmurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri={1}singlecomfirm&response_type=code&scope=snsapi_base&state={0}&connect_redirect=1#wechat_redirect".format(
        ID,url_encode)
    detailurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri={1}detail&response_type=code&scope=snsapi_base&state={0}#wechat_redirect".format(
        ID,url_encode)
    tempcloseurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri={1}tempclosealarm&response_type=code&scope=snsapi_base&state={0}&connect_redirect=1#wechat_redirect".format(
        ID,url_encode)
    send_values = [
        {
            "url": "{0}".format(detailurl),
            "title": "{0} {1}".format(_(ALARM_STATUS),ALARM_TITLE),
            "picurl": "{0}".format(imageurl)
        },
        {
            "title": "{4}:{1}({2})\n{5}:{3}".format(ALARM_STATUS, HOST_NAME, HOSTCONN, TIME,_("Host"),_("Time")),
        },
        {
            "title": "{2}：{0}\nID:{1}".format(HOST_GROUP,ID,_("Region")),"picurl": "{0}".format(serverityimageurl),
        },
        {
            "title": "{1}:{0}".format(DUTY_ROSTER,_("On duty")),
        },

    ]
    
    if ALARM_STATUS == "PROBLEM":
        text = {"title": _("Confirm Alarm"), "url": "{0}".format(comfirmurl), }
        send_values.append(text)
    if  len(MESSAGE)!=0: 
        text = {"title": _("Alarm description:{0}").format(MESSAGE), }
        send_values.insert(3, text)
    if ONEDAYTIMES > 3 or ONEWEEKTIMES > 7:
        text = {
            "title":_("This alarm occurred {0} times in the last day,{1} times in the last week,Click on this to temporarily closed it for 12 hours").format(ONEDAYTIMES,ONEWEEKTIMES),"url": "{0}".format(tempcloseurl),  }
        send_values.append(text)
    toparty = findgroupid(HOST_GROUP)
    toagent = findagentid(HOST_GROUP)
    senddatanews(send_values,toparty,toagent)
