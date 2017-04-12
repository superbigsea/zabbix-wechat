#!/usr/bin/python3.4
# coding: utf-8
import urllib.request
import cgi
import cgitb
import sys
import json
import time
import os
import shutil
import logging
import os
import codecs
import re
import logging
import json
import base64
import http.cookiejar
import urllib.request
from urllib import request, parse

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

zabbix_server_charturl = "http://127.0.0.1/zabbix/chart.php"
ttserver = "http://www.example.com:1978"
server_url = "http://www.example.com/getvalue"
logging.basicConfig(
    filename='/var/log/zabbix/wechat.log',
    format='%(levelname)s:%(asctime)s:%(message)s',
    level=logging.INFO
)

def savepic(itemid, eventid):
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('/tmp/zabbix_cookie', ignore_discard=True, ignore_expires=True)
    data = {
        "itemids": '{0}'.format(itemid),
        "period": "3600",
        "stime": "0",
        "width": "800"}
    data = parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(zabbix_server_charturl, data=data)
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    req = urllib.request.Request(
        url='{1}/{0}.png'.format(eventid, ttserver), data=response.read(), method='PUT')
    urllib.request.urlopen(req)

logging.info(sys.argv[1])
message = sys.argv[1]

alarm_title = message.split("@@@")[0]
triggerdescription = message.split("@@@")[1]
host_name = message.split("@@@")[2]
triggerseverity = message.split("@@@")[3]
itemid = message.split("@@@")[4]
alarm_status = message.split("@@@")[5]
hostconn = message.split("@@@")[6]
host_group = message.split("@@@")[7]
eventid = message.split("@@@")[8]
with open('/etc/zabbix/pub.key') as f:
    key = f.read()
rsakey = RSA.importKey(key)
cipher = Cipher_pkcs1_v1_5.new(rsakey)
postdata = {
    "host_group": "{0}".format(host_group),
    "eventid": "{0}".format(eventid),
    "alarm_title": "{0}".format(alarm_title),
    "triggerdescription": "{0}".format(triggerdescription),
    "host_name": "{0}".format(host_name),
    "triggerseverity": "{0}".format(triggerseverity),
    "alarm_status": "{0}".format(alarm_status),
    "hostconn": "{0}".format(hostconn)}
cipher_text = base64.b64encode(cipher.encrypt(str(postdata).encode()))
logging.info(postdata)
postdata = {"data": cipher_text.decode()}
postdata = urllib.parse.urlencode(postdata)
postdata = postdata.encode('utf-8')
url = server_url
res = urllib.request.urlopen(url, postdata)
ID = res.read().decode()
if alarm_status == "PROBLEM" and "[text]" not in alarm_title:
    savepic(itemid, ID)
logging.info("ID:{0}".format(ID))
