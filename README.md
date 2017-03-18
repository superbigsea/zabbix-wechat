# zabbix-wechat

------

作者:superbigsea 邮箱:29338383@qq.com qq群238705984

做出来的效果 http://mp.weixin.qq.com/s?__biz=MzIzNjUxMzk2NQ==&mid=2247484693&idx=1&sn=ae7482230a90476f912eaada2849c861&chksm=e8d7fad7dfa073c17b364e15fe4464d2b1f09a49fcc66906856e72ff15cc2b7fc183af7f225a&mpshare=1&scene=23&srcid=0228sGfPKDoLskzjzaMv5j1b#rd



------

## 一、简介

本项目目的是在微信端搭建一个兼容各个监控系统的统一报警处理系统，能实现报警提醒，报警压缩，报警分类，报警汇总报表等功能。主服务器实质上是一台位于公网上的http服务器，位于各地的zabbix server将报警信息经过初步处理后通过http post请求将信息传送至主服务器，主服务器将信息经过一定的处理再完成和微信端（报警接受者）进行处理，目前尚处于初级阶段，上文中的功能都可以实现，需要使用者有一定的linux、python、zabbix基础。
## 二 流程
![](https://github.com/superbigsea/zabbix-wechat/blob/master/%E6%8A%A5%E8%AD%A6%E6%B5%81%E7%A8%8B.png)

## 三 所需要的组件

### 1、zabbix server端报警脚本，主要将zabbix server传递过来的报警信息进行一定的格式处理，进行需要python3的支持
### 2、主服务器：采用python3+django
### 3、其他组件：mysql、redis（缓存微信token，也可以用memcacahed）、tt server（用来存放报警的图片和文字信息，不考虑高可用的话直接用Apache也可以）
### 4、一个二级域名 
### 5、一个微信企业号
## 四 安装部署
### zabbix server 报警插件
1、生成密钥对  
``` shell
ssh-keygen -b 4096 -t rsa -f /etc/zabbix/pub
mv /etc/zabbix/pub.pub /etc/zabbix/pub.key
```
