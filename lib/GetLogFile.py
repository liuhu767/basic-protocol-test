#!/usr/bin/python
#coding:utf-8
import requests
import json
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class GetLogFile(object):

    def __init__(self, deviceid, starTime, endTime):
        datetime_start = datetime.datetime.strptime(starTime, "%Y-%m-%d %H:%M:%S")
        datetime_end = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        start = time.mktime(datetime_start.timetuple())
        end = time.mktime(datetime_end.timetuple())
        url_format = 'xxxxxx'
        print start
        print end
        url = url_format % (start, end, deviceid)
        print url
        res = requests.get(url)
        print res.encoding
        bodys = json.loads(res.text, encoding="utf-8")
        fd = open('./0731.log', 'wb')
        for item in bodys:
            fd.write((item['body']).encode('utf-8') + '\n')
        fd.close()

if __name__ == "__main__":
    startTime = "2018-07-31 18:10:00"
    endTime = "2018-07-31 18:20:00"
    deviceid = 'xxxxxx' 
    glf = GetLogFile(deviceid, startTime, endTime)
