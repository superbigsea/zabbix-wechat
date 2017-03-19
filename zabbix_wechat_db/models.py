from django.db import models


class ALARM_INFO(models.Model):
    ALARM_ID = models.CharField(max_length=32)
    ALARM_TITLE = models.CharField(max_length=512)
    ALARM_TIME = models.CharField(max_length=32)
    MESSAGE = models.CharField(max_length=512)
    CONFIRM_TIME = models.CharField(max_length=32)
    CONFIRM_USER_ID = models.CharField(max_length=32)
    RESOLVE_TIME = models.CharField(max_length=32)
    HOST_NAME = models.CharField(max_length=32)
    RESOLVE_PERIOD = models.CharField(max_length=32)
    CONFIRM_PERIOD = models.CharField(max_length=32)
    SEVERITY = models.CharField(max_length=32)
    ALARM_TYPE = models.CharField(max_length=32)
    ALARM_STATUS = models.CharField(max_length=32)
    ADDIN = models.CharField(max_length=32)
    REMOVED = models.CharField(max_length=32)
    REL_WECHAT = models.CharField(max_length=32)
    HOST_GROUP = models.CharField(max_length=32)
    COMPRESSED_BY_TIME = models.CharField(max_length=32)
    COMPRESSED_BY_KEYWORD = models.CharField(max_length=32)
    COMPRESSED_BY_KEYWORD = models.CharField(max_length=32)
    COMPRESSED_BY_HOST = models.CharField(max_length=32)




class DUTY_ROSTER(models.Model):
    NICK_NAME = models.CharField(max_length=64)


class GROUP(models.Model):
    GROUPNAME = models.CharField(max_length=32)
    PARTY = models.CharField(max_length=64)
    AGENTID = models.CharField(max_length=64,default='')


class TEMP_CLOSED(models.Model):
    BEGINTIME = models.CharField(max_length=32)
    ENDTIME = models.CharField(max_length=32)
    HOST_NAME = models.CharField(max_length=32)
    HOST_GROUP = models.CharField(max_length=32)
    ALARM_TITLE = models.CharField(max_length=512)
    REMOVED = models.CharField(max_length=32)
    USER_ID = models.CharField(max_length=32)
    
class ALARM_DEPEND(models.Model):
    ALARM_TITLE = models.CharField(max_length=32)
    ALARM_DEPEND_TITLE = models.CharField(max_length=32)

