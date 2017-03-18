# zabbix-wechat

------

作者:superbigsea 邮箱:29338383@qq.com qq群238705984
做出来的效果 http://mp.weixin.qq.com/s?__biz=MzIzNjUxMzk2NQ==&mid=2247484693&idx=1&sn=ae7482230a90476f912eaada2849c861&chksm=e8d7fad7dfa073c17b364e15fe4464d2b1f09a49fcc66906856e72ff15cc2b7fc183af7f225a&mpshare=1&scene=23&srcid=0228sGfPKDoLskzjzaMv5j1b#rd



------

## 一、简介

本项目目的是在微信端搭建一个兼容各个监控系统的统一报警处理系统，能实现报警提醒，报警压缩，报警分类，报警汇总报表等功能。

## 二 流程


```flow
st=>start: zabbix触发报警

op=>operation: 生成历史图


st->op->e

```
