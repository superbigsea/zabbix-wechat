# zabbix-wechat

------

作者:superbigsea 邮箱:superbigsea@sina.com qq群238705984

做出来的效果 http://mp.weixin.qq.com/s?__biz=MzIzNjUxMzk2NQ==&mid=2247484693&idx=1&sn=ae7482230a90476f912eaada2849c861&chksm=e8d7fad7dfa073c17b364e15fe4464d2b1f09a49fcc66906856e72ff15cc2b7fc183af7f225a&mpshare=1&scene=23&srcid=0228sGfPKDoLskzjzaMv5j1b#rd



------

# Introduction

The purpose of this project is to build an alarm infomation system that is compatible with each monitoring system，and also can  reminder alarm, alarm compression, alarm classification, alarm summary report and other functions。Readers need to have some linux, python, zabbix experience。
# Flow
![](https://github.com/superbigsea/zabbix-wechat/blob/master/4.PNG)

# The required components

## 1、zabbix server端报警脚本，主要将zabbix server传递过来的报警信息进行一定的格式处理，进行需要python3的支持
## 2、主服务器：采用python3+django
## 3、其他组件：mysql、redis（用来缓存微信token，也可以用memcacahed）、tt server（用来存放报警的图片和文字信息，不考虑高可用的话直接用Apache也可以）
## 4、一个开启了80和1978端口的二级域名 
## 5、一个微信企业号
# 四 安装部署 
 
 整个安装配置较为复杂，使用的组件较多
## (一)zabbix server 报警插件
### 1、安装python3 和相关插件
``` shell
 yum install python34 python34-pip python34-devel
pip3 install  pycrypto
```
### 1、生成密钥对 
``` shell
ssh-keygen -b 4096 -t rsa -f /etc/zabbix/pub
mv /etc/zabbix/pub.pub /etc/zabbix/pub.key
```
### 2、安装python3将zabbix_alarm_script/all.py拷贝到zabbix的alertscripts目录，编辑下面3个地方
``` shell
zabbix_server_charturl = "http://127.0.0.1/zabbix/chart.php"  ##zabbix server 绘图接口
ttserver = "http://www.example.com:1978"   ##公网的ttserver 安装步骤见下面
server_url = "http://www.example.com/getvalue" ##公网的主服务器接口
```
### 3、生成cookies
``` shell
curl -c /tmp/zabbix_cookie -d "name=Admin&password=zabbix&autologin=1&enter=Sign+in"  http://127.0.0.1/zabbix/index.php
```
地址更改为zabbix server的地址，生成cookie的目的是便于脚本绘图时候不用认证了。
### 5、配置zabbix的action
``` shell
{TRIGGER.NAME}@@@{TRIGGER.DESCRIPTION}@@@{HOSTNAME}@@@{TRIGGER.SEVERITY}@@@{ITEM.ID}@@@{TRIGGER.STATUS}@@@{HOST.CONN}@@@{TRIGGER.HOSTGROUP.NAME}@@@{EVENT.ID}@@@
```
![](https://github.com/superbigsea/zabbix-wechat/blob/master/1.PNG)
![](https://github.com/superbigsea/zabbix-wechat/blob/master/2.PNG)
action 只需要传送一个参数，

## （二）mysql server 安装
``` shell
yum install mariadb-server -y
systemctl enable mariadb
systemctl start mariadb
CREATE DATABASE `alarm` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; #
grant all privileges on *.* to alarm@localhost identified by 'alarm';
```
## （三）redis server 安装
``` shell
yum install redis
systemctl enable redis
systemctl start redis
```
## （四）ttserver 安装 
``` shell
yum install bzip2-devel gcc zlib-devel -y
wget http://fallabs.com/tokyotyrant/tokyotyrant-1.1.41.tar.gz
wget http://fallabs.com/tokyocabinet/tokyocabinet-1.4.48.tar.gz
tar zxvf tokyocabinet-1.4.48.tar.gz
cd tokyocabinet-1.4.48
./configure
make && make install 
 tar zxvf tokyotyrant-1.1.41.tar.gz
 cd tokyotyrant-1.1.41
 ./configure
make && make install 
mkdir /ttdata/
./ttserver -port 1978 -thnum 8 -tout 30 -dmn -pid /ttdata/tt.pid -kl -log /ttdata/tt.log -le -ulog /ttdata -ulim 128m -sid 1 -rts /ttdata/tt.rts /ttdata/ttdb.tch

```
## （五）python3+django 安装 以及其他配置
``` shell
 yum install python34 python34-pip python34-devel
pip3 install django  pymysql django_crontab redis  pycrypto
```
### 1、将 上一节中生成的私钥文件 copy到 /etc/zabbix/pri.key
### 2 、编辑/etc/zabbix/wechat.conf
``` shell
[wechat]
corp_id=******************
corp_secret=*******************
toparty=***********
agentid=*************
url=http://**************
[redis]
host=****
port=****
```
其中上面4条为微信企业号的配置，可以参考https://github.com/X-Mars/Zabbix-Alert-WeChat
url 为服务器80端口的域名 
### 2、配置数据库连接
```
vim zabbixwechat/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'alarm',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'alarm',
        'PASSWORD': 'alarm',
        'HOST': 'alarm',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

``` 
### 3、初始化数据库
python3  manage.py  makemigrations
### 4、微信企业号菜单配置

发消息的权限，依然参考https://github.com/X-Mars/Zabbix-Alert-WeChat
如果要在微信菜单添加 汇总表

 先增加可信域名
 ![](https://github.com/superbigsea/zabbix-wechat/blob/master/3.PNG)
在微信菜单中添加网页跳转

设置如下
https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7dec596b2599614c&redirect_uri=http%3a%2f%2f*********%2fall&response_type=code&scope=snsapi_base&state=1&connect_redirect=1#wechat_redirect

把*******替换为 经过urlencode的域名

http://tool.chinaz.com/tools/urlencode.aspx 这个网址可以encode域名

### 5、运行程序

python3  manage.py runserver 0.0.0.0:80



