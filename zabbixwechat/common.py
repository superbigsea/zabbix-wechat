#!/usr/local/bin/python3.5
# coding:utf-8
import urllib.request
import json
import configparser
import pymysql
import time
import logging
import sys
import sqlalchemy
import codecs
import memcache
import gettext
import os
from zabbix_wechat_db.models import *
logging.basicConfig(
    filename='/var/log/zabbix/wechat.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
cf = configparser.ConfigParser()
cf.read("/etc/zabbix/wechat.conf")

def callgettext():
    
    return gettext.translation('django', localedir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'locale'), languages=[cf.get("wechat", "language")]).install(True)
     
    

def gettoken():
    memcached_host=cf.get("memcached", "host")
    try:
        mc = memcache.Client(memcached_host)
        if mc.get('weixintoken')==None:
            corp_id = cf.get("wechat", "corp_id")
            corp_secret = cf.get("wechat", "corp_secret")
            gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + \
                corp_id + '&corpsecret=' + corp_secret
            token_file = urllib.request.urlopen(gettoken_url)
            token_data = token_file.read().decode('utf-8')
            token_json = json.loads(token_data)
            token_json.keys()
            token = token_json['access_token']
            mc.set('weixintoken',token,time=7000)
        else:
            token = mc.get('weixintoken')
    except Exception as e:
            corp_id = cf.get("wechat", "corp_id")
            corp_secret = cf.get("wechat", "corp_secret")
            gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + \
                corp_id + '&corpsecret=' + corp_secret
            token_file = urllib.request.urlopen(gettoken_url)
            token_data = token_file.read().decode('utf-8')
            token_json = json.loads(token_data)
            token_json.keys()
            token = token_json['access_token']
    return token
def findgroupidfromwechat(groupname):
    party = cf.get("wechat", "toparty")
    access_token = gettoken()
    agentid = cf.get("wechat", "agentid")
    getuserinfo_url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={0}&id={1}'.format(
        access_token, agentid)
    logging.info(getuserinfo_url)
    userinfo_data = urllib.request.urlopen(
        getuserinfo_url).read().decode('utf-8') 
    userinfo = json.loads(userinfo_data)
    for i in userinfo['department']:
        if i["name"]==groupname:
            return i["id"]
def findgroupid(groupname):
    if len(GROUP.objects.filter(GROUPNAME=groupname))==0:
        return "3"
    else:
        return GROUP.objects.filter(GROUPNAME=groupname)[0].PARTY
def findagentid(groupname):
    if len(GROUP.objects.filter(GROUPNAME=groupname))==0:
        return "1"
    else:
        return GROUP.objects.filter(GROUPNAME=groupname)[0].AGENTID
def findgroupidbyagentid(agentid):
    if len(GROUP.objects.filter(AGENTID=agentid))==0:
        return "3"
    else:
        return GROUP.objects.filter(AGENTID=agentid)[0].PARTY


def findnickname(userid):
    party = cf.get("wechat", "toparty")
    access_token = gettoken()
    getuserinfo_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={0}&userid={1}'.format(
        access_token, userid)
    logging.info(getuserinfo_url)
    userinfo_data = urllib.request.urlopen(
        getuserinfo_url).read().decode('utf-8')
    userinfo = json.loads(userinfo_data)
    return userinfo['name']


def getusername(code):
    access_token = gettoken()
    getusername_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={0}&code={1}'.format(
        access_token, code)
    logging.info(code)
    user_file = urllib.request.urlopen(getusername_url)
    user_data = user_file.read().decode('utf-8')
    logging.info(user_data)
    user_json = json.loads(user_data)
    user_json.keys()
    user = user_json['UserId']
    return user


def getdutyroster():
    result = DUTY_ROSTER.objects.all()
    list = ''
    for i in result:
        list += i.NICK_NAME
        list += ","
    return list[:-1]
    

def senddata(content,toparty=cf.get("wechat", "toparty"),agentid = cf.get("wechat", "agentid")):
    access_token = gettoken()
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "toparty": "{0}".format(toparty),
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": content
        },
        "safe": "0"
    }
    logging.info(send_values)
    send_data = json.dumps(
        send_values,
        ensure_ascii=False).encode(
        encoding='UTF8')
    send_request = urllib.request.Request(send_url, send_data)
    response = urllib.request.urlopen(send_request)
    logging.info(response.read())


def senddatanews(content,toparty=cf.get("wechat", "toparty"),agentid = cf.get("wechat", "agentid")):
    access_token = gettoken()
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "toparty": "{0}".format(toparty),
        "msgtype": "news",
        "agentid": agentid,
        "news": {
            "articles": content
        }
    }
    logging.info(send_values)
    send_data = json.dumps(
        send_values,
        ensure_ascii=False).encode(
        encoding='UTF8')
    send_request = urllib.request.Request(send_url, send_data)
    response = urllib.request.urlopen(send_request)
    logging.info(response.read())
# def query_db(query_string):
#    logging.info(query_string.encode())
#    connection_string=cf.get("database","connection")
#    engine = sqlalchemy.create_engine(connection_string)
#    res = engine.execute(query_string)
#    return res
