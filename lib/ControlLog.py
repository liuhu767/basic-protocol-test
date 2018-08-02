#!/usr/bin/python
#coding:utf-8
import time
import datetime
import collections
import re
import os
import json
import requests

class ControlLog(object):
    def __init__(self):
        self.pingDict = dict()
        self.eventDict = dict() 
        self.directiveDict = dict() 
        self.directivechannelDict = dict() #stop
        self.device_id = ""
        self.logs = []

    def downloadLog(self, deviceid, starTime, endTime):
        datetime_start = datetime.datetime.strptime(starTime, "%Y-%m-%d %H:%M:%S")
        datetime_end = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        url_format = 'xxx'
        url = url_format % (datetime_start, datetime_end, device_id)
        print url
        res = requests.get(url)
        bodys = json.loads(res.text)
        return bodys

    def sortDict(self):
        self.pingDict = collections.OrderedDict(sorted(self.pingDict.items()))
        self.eventDict = collections.OrderedDict(sorted(self.eventDict.items()))
        self.directiveDict = collections.OrderedDict(sorted(self.directiveDict.items()))
#        self.directivechannelDict = collections.OrderedDict(sorted(self.directivechannelDict.items()))
        return

    def setFilterKeyWord(self, path, device_id, starTime, endTime):
        self.device_id = device_id
        #self.logdict = collections.OrderedDict()
        self.logs = self.getLogFiles(path)
        self.filterLogfileByTime(startTime, endTime)

    def setFilterDeviceid(self, deviceid):
        self.device_id = deviceid

    def getLogFiles(self, path):
        logFileList = list()
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.find("node.log") != -1:
                    logFileList.append(os.path.join(root, name))
        return logFileList

    def extractCommonSec(self, line):
        common_sec_list = ["logtime", "logid", "client_ip", "device_id", "dumi_uid", "baidu_uid"]
        tmpdict = dict()
        for one_sec in common_sec_list:
            idx = line.find(one_sec)
            if idx != -1:
                idx0 = line.find(" ", idx)
                if idx0 != -1:
                    sts = line[idx:idx0].split(":")
                    tmpdict[sts[0]] = sts[1]
                else:
                    sts = line[idx:len(line)].split(":")
                    tmpdict[sts[0]] = sts[1]
        return tmpdict

    # 提取事件
    def extractEvent(self, line):
        '''
        if line is Event ,we extract request
        '''
        tmpdict = self.extractCommonSec(line)
        # 将日志中pv_lost的值1的情况，即语音请求失败的日志过滤掉
        if "pv_lost:0" in line:
            log_data = line.split(" ")
            for i in range(len(log_data)):
                if str(log_data[i]).startswith("query:") and len(log_data[i][6:]) > 3:
                    tmpdict["asr_text"] = log_data[i][6:]
                if str(log_data[i]).startswith("request:") and len(log_data[i][8:]) > 3:
                    request_result = json.loads(log_data[i][8:])
                    tmpdict["request"] = str(json.dumps(request_result))
        return tmpdict

    # 提取指令
    def extractDirective(self, line):
        '''
        if line is DIRECTIVES, we extract response
        '''
        tmpdict = self.extractCommonSec(line)
        if 'pv_lost:0' in line:
            log_data = line.split(" ")
            for i in range(len(log_data)):
                if str(log_data[i]).startswith("response:") and len(log_data[i][9:]) > 3:
                    response_result = json.loads(log_data[i][9:])
                    tmpdict["response"] = str(json.dumps(response_result))
        return tmpdict

    def extractDirectiveDownchannel(self, line):
        '''
        if line is DIRECTIVES-DOWNCHANNEL , we extract response
        StopCapture or StopListen
        '''
#        pass
#        print 'extractDirectiveDownchannel'
    def getLogTimestamp(self, line):
        pattern = r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})" 
        mat = re.search(pattern, line)
        if mat is not None and len(mat.groups()) >= 1:
            timestr = mat.group(1)
            local_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
            local_timestamp = long(time.mktime(local_datetime.timetuple()) * 1000.0 + local_datetime.microsecond / 1000.0)
            return local_timestamp
        else:
            return 0

    def filterLogfileByTime(self, startTime, endTime):
        startTime = startTime + " " + "00:00:00"
        endTime = endTime + " " + "23:59:59"
        startTime = time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S"))
        endTime = time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S"))
        for logfile in self.logs:
            splist = logfile.split(".")
            if len(splist) == 2:
                logfileTime = time.mktime(time.strptime(splist[1], "%Y%m%d%H"))
                if logfileTime < startTime or logfileTime > endTime:
                    self.logs.remove(logfile)
            else:
                self.logs.remove(logfile)

    def filterLogInfDcsMain(self, line):
        if line.find("[INFO] dcs_main") != -1: 
            return True

    def filterDictTime(self, logdict, beginTime, endTime):
        '''
        beginTime / endTime format : 2017-09-27 16:44:03.535
        '''
        bTime = datetime.datetime.strptime(beginTime, "%Y-%m-%d %H:%M:%S.%f")
        eTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S.%f")
        return {k: v for k, v in logdict.items() if k >= bTime and k <= eTime}

    def filterByKeyWork(self, line):
        if line.find('[DEBUG]') != -1:
            return False, None
#        pattern_list = [r'\[DCS-PING\]', r'\[DCS-EVENTS\]', r'\[DCS-DIRECTIVES-DOWNCHANNEL\]', r'\[DCS-DIRECTIVES\]']
#        for item in pattern_list:
#            mat = re.search(item, line)
#            if mat is not None:
#                return True, mat.group()
#        return False, None

    def filterByDeviceId(self, line):
        pattern = self.device_id
        mat = re.search(pattern, line, re.I)
        if mat is not None and len(mat.group()) >= 1:
            return True
        return False

    def translogsToDict(self):
        for logfile in self.logs:
            self.transLogFileDict(logfile)

    def transLogFileDict(self, logfile):
        with open(logfile) as fd:
            for line in fd.readlines():
                if not self.filterByDeviceId(line):
                    continue
                logLineTime = self.getLogTimestamp(line)
                tmpDictEvent = self.extractEvent(line)
                tmpDictEvent['logtime'] = logLineTime 
                self.eventDict[logLineTime] = tmpDictEvent

                tmpDictDirective = self.extractDirective(line)
                tmpDictDirective['logtime'] = logLineTime
                self.directiveDict[logLineTime] = tmpDictDirective

    def pprint(self, logdict):
        for k, v in logdict.items():
            print k, v, len(v), "***"

    #获取event
    def getEventSet(self, eventDict):
        eventSet = set()
        namespace_list = ['ai.dueros.device_interface.voice_input', 'ai.dueros.device_interface.voice_output',
                          'ai.dueros.device_interface.speaker_controller', 'ai.dueros.device_interface.audio_player',
                          'ai.dueros.device_interface.playback_controller', 'ai.dueros.device_interface.alerts',
                          'ai.dueros.device_interface.system']
        name_list = ['ListenStarted', 'SpeechStarted', 'SpeechFinished', 'VolumeChanged',
                     'MuteChanged', 'PlaybackStarted', 'PlaybackFinished', 'PlaybackNearlyFinished',
                     'ProgressReportDelayElapsed', 'ProgressReportIntervalElapsed',
                     'PlaybackStutterStarted', 'PlaybackStutterFinished', 'PlaybackStopped',
                     'PlaybackPaused', 'PlaybackResumed', 'PlayCommandIssued', 'PauseCommandIssued',
                     'NextCommandIssued', 'PreviousCommandIssued', 'SetAlertSucceeded',
                     'SetAlertFailed', 'DeleteAlertSucceeded', 'AlertStarted', 'AlertStopped',
                     'AlertEnteredForeground', 'AlertEnteredBackground', 'SynchronizeState',
                     'UserInactivityReport', 'ResetUserInactivity']
        state_list = ['PlaybackState', 'ViewState', 'AlertsState', 'VolumeState', 'SpeechState']
        upload_event_list = ['ListenStarted', 'SynchronizeState', 'PlayCommandIssued', 'PauseCommandIssued',
                             'NextCommandIssued', 'PreviousCommandIssued']
        dataEventSet = set()
        name_in_voice_input = ['ListenStarted', 'ListenTimedOut']
        name_in_voice_output = ['SpeechStarted', 'SpeechFinished']

        for key, value in eventDict.items():
            state_list = ['PlaybackState', 'ViewState', 'AlertsState', 'VolumeState', 'SpeechState']
            #event在request中
            if value.has_key('request'):
                namespace = json.loads(value['request'])['event']['header']['namespace']
                name = json.loads(value['request'])['event']['header']['name']
                
                if 'clientContext' in value['request']:
                    # 遍历json.loads(value['response'])，因为会存在header相同的情况
                    for index in range(len(json.loads(value['request'])['clientContext'])):
                        # SpeechState_payload_token
                        if name in upload_event_list and 'SpeechState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            event_state_name = name + '_SpeechState'
                            # 校验name和namespace是否一一对应
                            if json.loads(value['request'])['clientContext'][index]['header']['namespace'] == 'ai.dueros.device_interface.voice_output':
                                pass
                            else:
                                print event_state_name + ' not correspond with ' + json.loads(value['request'])['clientContext'][index]['header']['namespace']

                            eventSet.add(event_state_name)
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'token' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    token = json.loads(value['request'])['clientContext'][index]['payload']['token']
                                    if len(str(token)) > 0:
                                        eventSet.add(event_state_name + "_payload_token")

                        # SpeechState_payload_offsetInMilliseconds
                        if name in upload_event_list and 'SpeechState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'offsetInMilliseconds' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    offsetInMilliseconds = json.loads(value['request'])['clientContext'][index]['payload']['offsetInMilliseconds']
                                    if len(str(offsetInMilliseconds)) > 0:
                                        event_state_name = name + 'SpeechState'
                                        eventSet.add(event_state_name + "_payload_offsetInMilliseconds")

                        # SpeechState_payload_playerActivity
                        if name in upload_event_list and 'SpeechState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                playerActivityList = ['PLAYING','FINISHED']
                                if 'playerActivity' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    playerActivity = json.loads(value['request'])['clientContext'][index]['payload']['playerActivity']
                                    if playerActivity in playerActivityList:
                                        event_state_name = name + 'SpeechState'
                                        eventSet.add(event_state_name + "_payload_playerActivity")


                        # VolumeState_payload_volume
                        if name in upload_event_list and 'VolumeState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            event_state_name = name + '_VolumeState'
                            # 校验name和namespace是否一一对应
                            if json.loads(value['request'])['clientContext'][index]['header']['namespace'] == 'ai.dueros.device_interface.speaker_controller':
                                pass
                            else:
                                print event_state_name + ' not correspond with ' + json.loads(value['request'])['clientContext'][index]['header']['namespace']

                            eventSet.add(event_state_name)
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'volume' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    volume = json.loads(value['request'])['clientContext'][index]['payload']['volume']
                                    if volume >= 0 and volume <= 100:
                                        eventSet.add(event_state_name + "_payload_volume")

                        # VolumeState_payload_muted
                        if name in upload_event_list and 'VolumeState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'muted' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    muted = json.loads(value['request'])['clientContext'][index]['payload']['muted']
                                    if 'false' == str(muted) or 'true' == str(muted):
                                        event_state_name = name + 'VolumeState'
                                        eventSet.add(event_state_name + "_payload_muted")


                        # PlaybackState_payload_token
                        if name in upload_event_list and 'PlaybackState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            event_state_name = name + '_PlaybackState'
                            # 校验name和namespace是否一一对应
                            #if json.loads(value['request'])['clientContext'][index]['header']['namespace'] == 'ai.dueros.device_interface.audio_player':
                            #    pass
                            #else:
                            #    print event_state_name + ' not correspond with ' + json.loads(value['request'])['clientContext'][index]['header']['namespace']

                            eventSet.add(event_state_name)
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'token' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    token = json.loads(value['request'])['clientContext'][index]['payload']['token']
                                    if len(str(token)) > 0:
                                        eventSet.add(event_state_name + "_payload_token")

                        # PlaybackState_payload_offsetInMilliseconds
                        if name in upload_event_list and 'PlaybackState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'offsetInMilliseconds' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    offsetInMilliseconds = json.loads(value['request'])['clientContext'][index]['payload']['offsetInMilliseconds']
                                    if offsetInMilliseconds != "":
                                        event_state_name = name + 'PlaybackState'
                                        eventSet.add(event_state_name + "_payload_offsetInMilliseconds")

                        # PlaybackState_payload_playerActivity
                        if name in upload_event_list and 'PlaybackState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                playerActivityList = ['PLAYING', 'STOPPED', 'PAUSED', 'BUFFER_UNDERRUN', 'FINISHED']
                                if 'playerActivity' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    playerActivity = json.loads(value['request'])['clientContext'][index]['payload']['playerActivity']
                                    if playerActivity in playerActivityList:
                                        event_state_name = name + 'PlaybackState'
                                        eventSet.add(event_state_name + "_payload_playerActivity")

                        # AlertsState_payload_allAlerts_token
                        if name in upload_event_list and 'AlertsState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            event_state_name = name + '_AlertsState'
                            # 校验name和namespace是否一一对应
                            if json.loads(value['request'])['clientContext'][index]['header']['namespace'] == 'ai.dueros.device_interface.alerts':
                                pass
                            else:
                                print event_state_name + ' not correspond with ' + json.loads(value['request'])['clientContext'][index]['header']['namespace']

                            eventSet.add(event_state_name)
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'allAlerts' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    for alertIndex in range(len(json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'])):
                                        if 'token' in json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'][alertIndex]:
                                            token = json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'][alertIndex]['token']
                                            if len(str(token)) > 0:
                                                eventSet.add(event_state_name + "_payload_allAlerts_token")

                        # AlertsState_payload_allAlerts_type
                        if name in upload_event_list and 'AlertsState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'allAlerts' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    for alertIndex in range(len(json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'])):
                                        if 'type' in json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'][alertIndex]:
                                            type = json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'][alertIndex]['type']
                                            if 'TIMER' == str(type) or 'ALARM' == str(type):
                                                event_state_name = name + 'AlertsState'
                                                eventSet.add(event_state_name + "_payload_allAlerts_type")

                        # AlertsState_payload_allAlerts_scheduledTime
                        if name in upload_event_list and 'AlertsState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'allAlerts' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    for alertIndex in range(len(json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'])):
                                        if 'scheduledTime' in json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'][alertIndex]:
                                            scheduledTime = json.loads(value['request'])['clientContext'][index]['payload']['allAlerts'][alertIndex]['scheduledTime']
                                            if scheduledTime.find("2018") != -1:
                                                event_state_name = name + 'AlertsState'
                                                eventSet.add(event_state_name + "_payload_allAlerts_scheduledTime")

                        # AlertsState_payload_activeAlerts_token
                        if name in upload_event_list and 'AlertsState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'activeAlerts' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    if len(json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts']) > 0:
                                        for alertIndex in range(len(json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'])):
                                            if 'token' in json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'][alertIndex]:
                                                token = json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'][alertIndex]['token']
                                                if len(str(token)) > 0:
                                                    event_state_name = name + 'AlertsState'
                                                    eventSet.add(event_state_name + "_payload_activeAlerts_token")

                        # AlertsState_payload_activeAlerts_type
                        if name in upload_event_list and 'AlertsState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'activeAlerts' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    if len(json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts']) > 0:
                                        for alertIndex in range(len(json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'])):
                                            if 'type' in json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'][alertIndex]:
                                                type = json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'][alertIndex]['type']
                                                if 'TIMER' == str(type) or 'ALARM' == str(type):
                                                    event_state_name = name + 'AlertsState'
                                                    eventSet.add(event_state_name + "_payload_activeAlerts_type")

                        # AlertsState_payload_activeAlerts_scheduledTime
                        if name in upload_event_list and 'AlertsState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'activeAlerts' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    if len(json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts']) > 0:
                                        for alertIndex in range(len(json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'])):
                                            if 'scheduledTime' in json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'][alertIndex]:
                                                scheduledTime = json.loads(value['request'])['clientContext'][index]['payload']['activeAlerts'][alertIndex]['scheduledTime']
                                                if scheduledTime.find("2018") != -1:
                                                    event_state_name = name + 'AlertsState'
                                                    eventSet.add(event_state_name + "_payload_activeAlerts_scheduledTime")

                        # ViewState_payload_token
                        if name in upload_event_list and 'ViewState' == json.loads(value['request'])['clientContext'][index]['header']['name']:
                            event_state_name = name + '_ViewState'
                            # 校验name和namespace是否一一对应
                            if json.loads(value['request'])['clientContext'][index]['header']['namespace'] == 'ai.dueros.device_interface.screen':
                                pass
                            else:
                                print event_state_name + ' not correspond with ' + json.loads(value['request'])['clientContext'][index]['header']['namespace']

                            eventSet.add(event_state_name)
                            if 'payload' in json.loads(value['request'])['clientContext'][index]:
                                if 'token' in json.loads(value['request'])['clientContext'][index]['payload']:
                                    token = json.loads(value['request'])['clientContext'][index]['payload']['token']
                                    if len(str(token)) > 0:
                                        eventSet.add(event_state_name + "_payload_token")

                        # 将没在开发平台上说明的状态打印出来
                        notContainStatesFile = open('not_contain_states.txt', 'a+')
                        if json.loads(value['request'])['clientContext'][index]['header']['name'] not in state_list:
                            state_str = str(json.loads(value['request'])['clientContext'][index]['header']) + '\n' + str(json.loads(value['request'])['clientContext'][index]['payload']) + '\n' + '---------------------------------------'
                            print>> notContainStatesFile, state_str
                        notContainStatesFile.close()

                # 校验name和namespace是否一一对应
                if name == 'ListenStarted':
                    if namespace == 'ai.dueros.device_interface.voice_input':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # ListenStarted_header_messageId
                if name == 'ListenStarted' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']
                    if len(str(messageId)) > 35:
                        eventSet.add("ListenStarted_header_messageId")

                # ListenStarted_header_dialogRequestId
                if name == 'ListenStarted' and 'dialogRequestId' in json.loads(value['request'])['event']['header']:
                    dialogRequestId = json.loads(value['request'])['event']['header']
                    if len(str(dialogRequestId)) > 35:
                        eventSet.add("ListenStarted_header_dialogRequestId")

                # ListenStarted_payload_format
                if name == 'ListenStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'format' in json.loads(value['request'])['event']['payload']:
                        format = json.loads(value['request'])['event']['payload']['format']
                        if 'AUDIO_L16_RATE_16000_CHANNELS_1' == format:
                            eventSet.add("ListenStarted_payload_format")

                # 校验name和namespace是否一一对应
                if name == 'SpeechStarted':
                    if namespace == 'ai.dueros.device_interface.voice_output':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # SpeechStarted_header_messageId
                if name == 'SpeechStarted' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']
                    if len(str(messageId)) > 35:
                        eventSet.add("SpeechStarted_header_messageId")

                # SpeechStarted_payload_token
                if name == 'SpeechStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("SpeechStarted_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'SpeechFinished':
                    if namespace == 'ai.dueros.device_interface.voice_output':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # SpeechFinished_header_messageId
                if name == 'SpeechFinished' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("SpeechFinished_header_messageId")

                # SpeechFinished_payload_token
                if name == 'SpeechFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("SpeechFinished_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'VolumeChanged':
                    if namespace == 'ai.dueros.device_interface.speaker_controller':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # VolumeChanged_header_messageId
                if name == 'VolumeChanged' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("VolumeChanged_header_messageId")

                # VolumeChanged_payload_volume
                if name == 'VolumeChanged' and 'payload' in json.loads(value['request'])['event']:
                    if 'volume' in json.loads(value['request'])['event']['payload']:
                        volume = json.loads(value['request'])['event']['payload']['volume']
                        if volume >= 0 and volume <= 100:
                            eventSet.add("VolumeChanged_payload_volume")

                # 校验name和namespace是否一一对应
                if name == 'MuteChanged':
                    if namespace == 'ai.dueros.device_interface.speaker_controller':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # VolumeChanged_payload_muted
                if name == 'MuteChanged' and 'payload' in json.loads(value['request'])['event']:
                    if 'muted' in json.loads(value['request'])['event']['payload']:
                        muted = json.loads(value['request'])['event']['payload']['muted']
                        if 'false' == str(muted) or 'true' == str(muted):
                            eventSet.add("MuteChanged_payload_muted")

                # MuteChanged_header_messageId
                if name == 'MuteChanged' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("MuteChanged_header_messageId")

                # MuteChanged_payload_volume
                if name == 'MuteChanged' and 'payload' in json.loads(value['request'])['event']:
                    if 'volume' in json.loads(value['request'])['event']['payload']:
                        volume = json.loads(value['request'])['event']['payload']['volume']
                        if volume >= 0 and volume <= 100:
                            eventSet.add("MuteChanged_payload_volume")

                # MuteChanged_payload_muted
                if name == 'MuteChanged' and 'payload' in json.loads(value['request'])['event']:
                    if 'muted' in json.loads(value['request'])['event']['payload']:
                        muted = json.loads(value['request'])['event']['payload']['muted']
                        if 'false' == muted or 'true' == muted:
                            eventSet.add("MuteChanged_payload_muted")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackStarted':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackStarted_header_messageId
                if name == 'PlaybackStarted' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackStarted_header_messageId")

                # PlaybackStarted_payload_token
                if name == 'PlaybackStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackStarted_payload_token")

                # PlaybackStarted_payload_offsetInMilliseconds
                if name == 'PlaybackStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackStarted_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackFinished':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackFinished_header_messageId
                if name == 'PlaybackFinished' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackFinished_header_messageId")

                # PlaybackFinished_payload_token
                if name == 'PlaybackFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackFinished_payload_token")

                # PlaybackFinished_payload_offsetInMilliseconds
                if name == 'PlaybackFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackFinished_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackNearlyFinished':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackNearlyFinished_header_messageId
                if name == 'PlaybackNearlyFinished' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackNearlyFinished_header_messageId")

                # PlaybackNearlyFinished_payload_token
                if name == 'PlaybackNearlyFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackNearlyFinished_payload_token")

                # PlaybackNearlyFinished_payload_offsetInMilliseconds
                if name == 'PlaybackNearlyFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackNearlyFinished_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'ProgressReportDelayElapsed':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # ProgressReportDelayElapsed_header_messageId
                if name == 'ProgressReportDelayElapsed' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("ProgressReportDelayElapsed_header_messageId")

                # ProgressReportDelayElapsed_payload_token
                if name == 'ProgressReportDelayElapsed' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("ProgressReportDelayElapsed_payload_allAlerts_token")

                # ProgressReportDelayElapsed_payload_offsetInMilliseconds
                if name == 'ProgressReportDelayElapsed' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("ProgressReportDelayElapsed_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'ProgressReportIntervalElapsed':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # ProgressReportIntervalElapsed_header_messageId
                if name == 'ProgressReportIntervalElapsed' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("ProgressReportIntervalElapsed_header_messageId")

                # ProgressReportIntervalElapsed_payload_token
                if name == 'ProgressReportIntervalElapsed' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("ProgressReportIntervalElapsed_payload_token")

                # ProgressReportDelayElapsed_payload_offsetInMilliseconds
                if name == 'ProgressReportIntervalElapsed' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("ProgressReportIntervalElapsed_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackStutterStarted':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackStutterStarted_header_messageId
                if name == 'PlaybackStutterStarted' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackStutterStarted_header_messageId")

                # PlaybackStutterStarted_payload_token
                if name == 'PlaybackStutterStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackStutterStarted_payload_allAlerts_token")

                # PlaybackStutterStarted_payload_offsetInMilliseconds
                if name == 'PlaybackStutterStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackStutterStarted_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackStutterFinished':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackStutterFinished_header_messageId
                if name == 'PlaybackStutterFinished' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackStutterFinished_header_messageId")

                # PlaybackStutterFinished_payload_token
                if name == 'PlaybackStutterFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackStutterFinished_payload_token")

                # PlaybackStutterFinished_payload_offsetInMilliseconds
                if name == 'PlaybackStutterFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackStutterFinished_payload_offsetInMilliseconds")

                # PlaybackStutterFinished_payload_stutterDurationInMilliseconds
                if name == 'PlaybackStutterFinished' and 'payload' in json.loads(value['request'])['event']:
                    if 'stutterDurationInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        stutterDurationInMilliseconds = json.loads(value['request'])['event']['payload']['stutterDurationInMilliseconds']
                        if len(str(stutterDurationInMilliseconds)) > 0:
                            eventSet.add("PlaybackStutterFinished_payload_stutterDurationInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackStopped':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackStopped_header_messageId
                if name == 'PlaybackStopped' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackStopped_header_messageId")

                # PlaybackStopped_payload_token
                if name == 'PlaybackStopped' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackStopped_payload_token")

                # PlaybackStopped_payload_offsetInMilliseconds
                if name == 'PlaybackStopped' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackStopped_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlaybackPaused':
                    if namespace == 'ai.dueros.device_interface.audio_player':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlaybackPaused_header_messageId
                if name == 'PlaybackPaused' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackPaused_header_messageId")

                # PlaybackPaused_payload_token
                if name == 'PlaybackPaused' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackPaused_payload_token")

                # PlaybackPaused_payload_offsetInMilliseconds
                if name == 'PlaybackPaused' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackPaused_payload_offsetInMilliseconds")

                # PlaybackResumed_header_messageId
                if name == 'PlaybackResumed' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlaybackResumed_header_messageId")

                # PlaybackResumed_payload_token
                if name == 'PlaybackResumed' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("PlaybackResumed_payload_allAlerts_token")

                # PlaybackResumed_payload_offsetInMilliseconds
                if name == 'PlaybackResumed' and 'payload' in json.loads(value['request'])['event']:
                    if 'offsetInMilliseconds' in json.loads(value['request'])['event']['payload']:
                        offsetInMilliseconds = json.loads(value['request'])['event']['payload']['offsetInMilliseconds']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("PlaybackResumed_payload_offsetInMilliseconds")

                # 校验name和namespace是否一一对应
                if name == 'PlayCommandIssued':
                    if namespace == 'ai.dueros.device_interface.playback_controller':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PlayCommandIssued_header_messageId
                if name == 'PlayCommandIssued' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PlayCommandIssued_header_messageId")

                # PauseCommandIssued_header_messageId
                if name == 'PauseCommandIssued' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PauseCommandIssued_header_messageId")

                # 校验name和namespace是否一一对应
                if name == 'NextCommandIssued':
                    if namespace == 'ai.dueros.device_interface.playback_controller':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # NextCommandIssued_header_messageId
                if name == 'NextCommandIssued' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("NextCommandIssued_header_messageId")

                # 校验name和namespace是否一一对应
                if name == 'PreviousCommandIssued':
                    if namespace == 'ai.dueros.device_interface.playback_controller':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # PreviousCommandIssued_header_messageId
                if name == 'PreviousCommandIssued' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("PreviousCommandIssued_header_messageId")

                # 校验name和namespace是否一一对应
                if name == 'SetAlertSucceeded':
                    if namespace == 'ai.dueros.device_interface.alerts':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # SetAlertSucceeded_header_messageId
                if name == 'SetAlertSucceeded' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("SetAlertSucceeded_header_messageId")

                # SetAlertSucceeded_payload_token
                if name == 'SetAlertSucceeded' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("SetAlertSucceeded_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'DeleteAlertSucceeded':
                    if namespace == 'ai.dueros.device_interface.alerts':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # DeleteAlertSucceeded_header_messageId
                if name == 'DeleteAlertSucceeded' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("DeleteAlertSucceeded_header_messageId")

                # DeleteAlertSucceeded_payload_token
                if name == 'DeleteAlertSucceeded' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("DeleteAlertSucceeded_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'AlertStarted':
                    if namespace == 'ai.dueros.device_interface.alerts':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # AlertStarted_header_messageId
                if name == 'AlertStarted' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("AlertStarted_header_messageId")

                # AlertStarted_payload_token
                if name == 'AlertStarted' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("AlertStarted_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'AlertStopped':
                    if namespace == 'ai.dueros.device_interface.alerts':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # AlertStopped_header_messageId
                if name == 'AlertStopped' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("AlertStarted_header_messageId")

                # AlertStopped_payload_token
                if name == 'AlertStopped' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("AlertStopped_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'AlertEnteredForeground':
                    if namespace == 'ai.dueros.device_interface.alerts':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # AlertEnteredForeground_payload_token
                if name == 'AlertEnteredForeground' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("AlertEnteredForeground_header_messageId")

                # AlertEnteredForeground_payload_token
                if name == 'AlertEnteredForeground' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("AlertEnteredForeground_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'AlertEnteredBackground':
                    if namespace == 'ai.dueros.device_interface.alerts':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # AlertEnteredBackground_payload_token
                if name == 'AlertEnteredBackground' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if len(str(token)) > 0:
                            eventSet.add("AlertEnteredBackground_payload_token ok")

                # AlertEnteredBackground_payload_token
                if name == 'AlertEnteredBackground' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("AlertEnteredBackground_header_messageId")

                # 校验name和namespace是否一一对应
                if name == 'LinkClicked':
                    if namespace == 'ai.dueros.device_interface.screen':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # LinkClicked_header_messageId
                if name == 'LinkClicked' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("LinkClicked_header_messageId")

                # LinkClicked_payload_url
                if name == 'LinkClicked' and 'payload' in json.loads(value['request'])['event']:
                    if 'url' in json.loads(value['request'])['event']['payload']:
                        url = json.loads(value['request'])['event']['payload']['url']
                        if type(url) == 'str' and url.startswith('http') > 0:
                            eventSet.add("LinkClicked_payload_url")

                # LinkClicked_payload_token
                if name == 'LinkClicked' and 'payload' in json.loads(value['request'])['event']:
                    if 'token' in json.loads(value['request'])['event']['payload']:
                        token = json.loads(value['request'])['event']['payload']['token']
                        if type(token) == 'str' and len(token) > 0:
                            eventSet.add("LinkClicked_payload_token")

                # 校验name和namespace是否一一对应
                if name == 'SynchronizeState':
                    if namespace == 'ai.dueros.device_interface.system':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # SynchronizeState_header_messageId
                if name == 'SynchronizeState' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("SynchronizeState_header_messageId")

                # 校验name和namespace是否一一对应
                if name == 'UserInactivityReport':
                    if namespace == 'ai.dueros.device_interface.system':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # UserInactivityReport_header_messageId
                if name == 'UserInactivityReport' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("UserInactivityReport")

                # UserInactivityReport_payload_inactiveTimeInSeconds
                if name == 'UserInactivityReport' and 'payload' in json.loads(value['request'])['event']:
                    if 'inactiveTimeInSeconds' in json.loads(value['request'])['event']['payload']:
                        inactiveTimeInSeconds = json.loads(value['request'])['event']['payload']['inactiveTimeInSeconds']
                        if len(str(inactiveTimeInSeconds)) > 0:
                            eventSet.add("UserInactivityReport_payload_inactiveTimeInSeconds")

                # 校验name和namespace是否一一对应
                if name == 'ExceptionEncountered':
                    if namespace == 'ai.dueros.device_interface.system':
                        cmd = namespace + '.' + name
                        eventSet.add(cmd)
                    else:
                        print name + ' not correspond with ' + namespace

                # ExceptionEncountered_header_messageId
                if name == 'ExceptionEncountered' and 'messageId' in json.loads(value['request'])['event']['header']:
                    messageId = json.loads(value['request'])['event']['header']['messageId']
                    if len(str(messageId)) > 35:
                        eventSet.add("ExceptionEncountered_header_messageId")

                # ExceptionEncountered_payload_unparsedDirective
                if name == 'ExceptionEncountered' and 'payload' in json.loads(value['request'])['event']:
                    if 'unparsedDirective' in json.loads(value['request'])['event']['payload']:
                        unparsedDirective = json.loads(value['request'])['event']['payload']['unparsedDirective']
                        if len(str(offsetInMilliseconds)) > 0:
                            eventSet.add("ExceptionEncountered_payload_unparsedDirective")

                # ExceptionEncountered_payload_error_type
                if name == 'ExceptionEncountered' and 'payload' in json.loads(value['request'])['event']:
                    if 'unparsedDirective' in json.loads(value['request'])['event']['payload']:
                       if 'error' in json.loads(value['request'])['event']['payload']['unparsedDirective']:
                           typeList = ['UNEXPECTED_INFORMATION_RECEIVED','UNSUPPORTED_OPERATION','INTERNAL_ERROR']
                           if 'type' in json.loads(value['request'])['event']['payload']['unparsedDirective']['error']:
                               type = json.loads(value['request'])['event']['payload']['unparsedDirective']['error']['type']
                               if type in typeList > 0:
                                   eventSet.add("ExceptionEncountered_payload_error_type")

                # ExceptionEncountered_payload_error_message
                if name == 'ExceptionEncountered' and 'payload' in json.loads(value['request'])['event']:
                    if 'unparsedDirective' in json.loads(value['request'])['event']['payload']:
                       if 'error' in json.loads(value['request'])['event']['payload']['unparsedDirective']:
                           if 'message' in json.loads(value['request'])['event']['payload']['unparsedDirective']['error']:
                               message = json.loads(value['request'])['event']['payload']['unparsedDirective']['error']['message']
                               if len(str(message)) > 0:
                                   eventSet.add("ExceptionEncountered_payload_error_message")

                # 输出不在开发平台上的事件
                notContainEventsFile = open('not_contain_events.txt', 'a+')
                if name not in name_list:
                    events_str = json.loads(value['request'])['event']
                    print>> notContainEventsFile, events_str
                notContainEventsFile.close()
                # if namespace in namespace_list and name in name_list:
                #       cmd = namespace + '.' + name
                #       eventSet.add(cmd)

        return eventSet

    # 获取directive
    def getDirectiveSet(self, directiveDict):
        directiveSet = set()
        namespace_list = ['ai.dueros.device_interface.voice_input', 'ai.dueros.device_interface.voice_output', 'ai.dueros.device_interface.speaker_controller', 'ai.dueros.device_interface.audio_player', 'ai.dueros.device_interface.alerts', 'ai.dueros.device_interface.screen']
        name_list = ['StopListen', 'Listen', 'Speak', 'SetVolume', 'AdjustVolume', 'SetMute', 'Play', 'Stop', 'SetAlert', 'DeleteAlert', 'HtmlView']
        dataSet = set()

        for key, value in directiveDict.items():
            # directive在response中
            if value.has_key('response') :
                if 'directive' in value['response']:
                    # 遍历json.loads(value['response'])，因为会存在directive相同的情况
                    for index in range(len(json.loads(value['response']))):
                        namespace = json.loads(value['response'])[index]['directive']['header']['namespace']
                        name = json.loads(value['response'])[index]['directive']['header']['name']

                        # 校验name和namespace是否一一对应
                        if name == 'StopListen':
                            if namespace == 'ai.dueros.device_interface.voice_input':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # StopListen_header_messageId
                        if name == 'StopListen' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 35:
                                    directiveSet.add('StopListen_header_messageId')

                        # StopListen_header_dialogRequestId
                        if name == 'StopListen' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('StopListen_header_dialogRequestId')

                        # 校验name和namespace是否一一对应
                        if name == 'Listen':
                            if namespace == 'ai.dueros.device_interface.voice_input':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # Listen_header_messageId
                        if name == 'Listen' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('Listen_header_messageId')

                        # Listen_header_dialogRequestId
                        if name == 'Listen' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('Listen_header_dialogRequestId')

                        # Listen_payload_timeoutInMilliseconds
                        if name == 'Listen' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'timeoutInMilliseconds' in json.loads(value['response'])[index]['directive']['payload']:
                                timeoutInMilliseconds = json.loads(value['response'])[index]['directive']['payload']['timeoutInMilliseconds']
                                if len(str(timeoutInMilliseconds)) > 0:
                                    directiveSet.add('Listen_payload_timeoutInMilliseconds')

                        # 校验name和namespace是否一一对应
                        if name == 'Speak':
                            if namespace == 'ai.dueros.device_interface.voice_output':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # Speak_header_messageId
                        if name == 'Speak' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('Speak_header_messageId')

                        # Speak_header_dialogRequestId
                        if name == 'Speak' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('Speak_header_dialogRequestId')

                        # Speak_payload_format
                        if name == 'Speak' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'format' in json.loads(value['response'])[index]['directive']['payload']:
                                format = json.loads(value['response'])[index]['directive']['payload']['format']
                                formatList = ['AUDIO_MPEG','AUDIO_L16_RATE_16000_CHANNELS_1']
                                if format in formatList:
                                    directiveSet.add('Speak_payload_format')

                        # Speak_payload_token
                        if name == 'Speak' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'token' in json.loads(value['response'])[index]['directive']['payload']:
                                token = json.loads(value['response'])[index]['directive']['payload']['token']
                                if len(str(token)) > 0:
                                    directiveSet.add('Speak_payload_token')

                        # Speak_payload_url
                        if name == 'Speak' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'url' in json.loads(value['response'])[index]['directive']['payload']:
                                url = json.loads(value['response'])[index]['directive']['payload']['url']
                                if str(url).startswith('http'):
                                    directiveSet.add('Speak_payload_url')

                        # 校验name和namespace是否一一对应
                        if name == 'SetVolume':
                            if namespace == 'ai.dueros.device_interface.speaker_controller':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # SetVolume_header_messageId
                        if name == 'SetVolume' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('SetVolume_header_messageId')

                        # SetVolume_header_dialogRequestId
                        if name == 'SetVolume' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('SetVolume_header_dialogRequestId')

                        # SetVolume_payload_volume
                        if name == 'SetVolume' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'volume' in json.loads(value['response'])[index]['directive']['payload']:
                                volume = json.loads(value['response'])[index]['directive']['payload']['volume']
                                if volume >= 0 and volume <= 100:
                                    directiveSet.add('SetVolume_payload_volume')

                        # 校验name和namespace是否一一对应
                        if name == 'AdjustVolume':
                            if namespace == 'ai.dueros.device_interface.speaker_controller':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # AdjustVolume_header_messageId
                        if name == 'AdjustVolume' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('AdjustVolume_header_messageId')

                        # AdjustVolume_header_dialogRequestId
                        if name == 'AdjustVolume' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('AdjustVolume_header_dialogRequestId')

                        # AdjustVolume_payload_volume
                        if name == 'AdjustVolume' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'volume' in json.loads(value['response'])[index]['directive']['payload']:
                                volume = json.loads(value['response'])[index]['directive']['payload']['volume']
                                if volume >= -100 and volume <= 100:
                                    directiveSet.add('AdjustVolume_payload_volume')

                        # 校验name和namespace是否一一对应
                        if name == 'SetMute':
                            if namespace == 'ai.dueros.device_interface.speaker_controller':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # SetMute_header_messageId
                        if name == 'SetMute' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('SetMute_header_messageId')

                        # SetMute_header_dialogRequestId
                        if name == 'SetMute' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 35:
                                    directiveSet.add('SetMute_header_dialogRequestId')

                        # SetMute_payload_mute
                        if name == 'SetMute' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'mute' in json.loads(value['response'])[index]['directive']['payload']:
                                mute = json.loads(value['response'])[index]['directive']['payload']['mute']
                                if 'False' == str(mute) or 'True' == str(mute):
                                    directiveSet.add('SetMute_payload_mute')

                        # 校验name和namespace是否一一对应
                        if name == 'Play':
                            if namespace == 'ai.dueros.device_interface.audio_player':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # Play_header_messageId
                        if name == 'Play' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                            if 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('Play_header_messageId')

                        # Play_header_dialogRequestId
                        if name == 'Play' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('Play_header_dialogRequestId')

                        # Play_payload_playBehavior_ENQUEUE_expectedPreviousToken
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'playBehavior' in json.loads(value['response'])[index]['directive']['payload']:
                                playBehavior = json.loads(value['response'])[index]['directive']['payload']['playBehavior']
                                if str(playBehavior) == 'ENQUEUE':
                                    if 'expectedPreviousToken' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        expectedPreviousToken = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['expectedPreviousToken']
                                        if len(str(expectedPreviousToken)) > 0:
                                            directiveSet.add('Play_payload_playBehavior_ENQUEUE_expectedPreviousToken')

                        # Play_payload_playBehavior_REPLACE_ENQUEUED_expectedPreviousToken
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'playBehavior' in json.loads(value['response'])[index]['directive']['payload']:
                                playBehavior = json.loads(value['response'])[index]['directive']['payload']['playBehavior']
                                if str(playBehavior) == 'REPLACE_ENQUEUED':
                                    if 'expectedPreviousToken' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        expectedPreviousToken = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['expectedPreviousToken']
                                        if len(str(expectedPreviousToken)) > 0:
                                            directiveSet.add('Play_payload_playBehavior_REPLACE_ENQUEUED_expectedPreviousToken')

                        # Play_payload_playBehavior_REPLACE_ALL
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'playBehavior' in json.loads(value['response'])[index]['directive']['payload']:
                                playBehavior = json.loads(value['response'])[index]['directive']['payload']['playBehavior']
                                if str(playBehavior) == 'REPLACE_ALL':
                                    if 'expectedPreviousToken' not in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        directiveSet.add('Play_payload_playBehavior_REPLACE_ALL')

                        # Play_payload_audioItem_audioItemId
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'audioItemId' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    audioItemId = json.loads(value['response'])[index]['directive']['payload']['audioItem']['audioItemId']
                                    if len(str(audioItemId)) > 0:
                                        directiveSet.add('Play_payload_audioItem_audioItemId')

                        # Play_payload_audioItem_stream_url
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'url' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        url = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['url']
                                        if str(url).startswith('http'):
                                            directiveSet.add('Play_payload_audioItem_stream_url')

                        # Play_payload_audioItem_stream_streamFormat
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'streamFormat' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        streamFormat = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['streamFormat']
                                        if streamFormat == 'AUDIO_MPEG':
                                            directiveSet.add('Play_payload_audioItem_stream_streamFormat')

                        # Play_payload_audioItem_stream_offsetInMilliseconds
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'offsetInMilliseconds' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        offsetInMilliseconds = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['offsetInMilliseconds']
                                        if len(str(offsetInMilliseconds)) > 0:
                                            directiveSet.add('Play_payload_audioItem_stream_offsetInMilliseconds')

                        # Play_payload_audioItem_stream_expiryTime
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'expiryTime' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        expiryTime = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['expiryTime']
                                        if expiryTime.startswith("2018"):
                                            directiveSet.add('Play_payload_audioItem_stream_expiryTime')

                        # Play_payload_audioItem_stream_progressReport_progressReportDelayInMilliseconds/progressReportIntervalInMilliseconds
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'progressReport' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        if 'progressReportDelayInMilliseconds' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['progressReport']:
                                            progressReportDelayInMilliseconds = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['progressReport']['progressReportDelayInMilliseconds']
                                            if len(str(progressReportDelayInMilliseconds)) > 0:
                                                directiveSet.add('Play_payload_audioItem_stream_progressReport_progressReportDelayInMilliseconds')

                                        if 'progressReportIntervalInMilliseconds' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['progressReport']:
                                            progressReportIntervalInMilliseconds = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['progressReport']['progressReportIntervalInMilliseconds']
                                            if len(str(progressReportIntervalInMilliseconds)) > 0:
                                                directiveSet.add('Play_payload_audioItem_stream_progressReport_progressReportIntervalInMilliseconds')
                                        
                        # Play_payload_audioItem_stream_token
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'token' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        token = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['token']
                                        if len(str(token)) > 0:
                                            directiveSet.add('Play_payload_audioItem_stream_token')

                        # Play_payload_audioItem_stream_expectedPreviousToken
                        if name == 'Play' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'audioItem' in json.loads(value['response'])[index]['directive']['payload']:
                                if 'stream' in json.loads(value['response'])[index]['directive']['payload']['audioItem']:
                                    if 'expectedPreviousToken' in json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']:
                                        expectedPreviousToken = json.loads(value['response'])[index]['directive']['payload']['audioItem']['stream']['expectedPreviousToken']
                                        if len(str(expectedPreviousToken)) > 0:
                                            dataSet.add('Play_payload_audioItem_stream_expectedPreviousToken')

                        # 校验name和namespace是否一一对应
                        if name == 'Stop':
                            if namespace == 'ai.dueros.device_interface.audio_player':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # Stop_header_messageId
                        if name == 'Stop' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('Stop_header_messageId')

                        # Stop_header_dialogRequestId
                        if name == 'Stop' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('Stop_header_dialogRequestId')

                        # 校验name和namespace是否一一对应
                        if name == 'SetAlert':
                            if namespace == 'ai.dueros.device_interface.alerts':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # SetAlert_header_messageId
                        if name == 'SetAlert' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('SetAlert_header_messageId')

                        # SetAlert_header_dialogRequestId
                        if name == 'SetAlert' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('SetAlert_header_dialogRequestId')

                        # SetAlert_payload_token
                        if name == 'SetAlert' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'token' in json.loads(value['response'])[index]['directive']['payload']:
                                token = json.loads(value['response'])[index]['directive']['payload']['token']
                                if len(str(token)) > 0:
                                    directiveSet.add('SetAlert_payload_token')

                        # SetAlert_payload_type
                        if name == 'SetAlert' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'type' in json.loads(value['response'])[index]['directive']['payload']:
                                type = json.loads(value['response'])[index]['directive']['payload']['type']
                                if str(type) == 'TIMER' or str(type) == 'ALARM':
                                    directiveSet.add('SetAlert_payload_type')

                        # SetAlert_payload_scheduledTime
                        if name == 'SetAlert' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'scheduledTime' in json.loads(value['response'])[index]['directive']['payload']:
                                scheduledTime = json.loads(value['response'])[index]['directive']['payload']['scheduledTime']
                                if scheduledTime.startswith("2018"):
                                    directiveSet.add('SetAlert_payload_scheduledTime')

                        # 校验name和namespace是否一一对应
                        if name == 'DeleteAlert':
                            if namespace == 'ai.dueros.device_interface.alerts':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # DeleteAlert_header_messageId
                        if name == 'DeleteAlert' and 'messageId' in json.loads(value['response'])[index]['directive']['header']:
                                messageId = json.loads(value['response'])[index]['directive']['header']['messageId']
                                if len(str(messageId)) > 0:
                                    directiveSet.add('DeleteAlert_header_messageId')

                        # DeleteAlert_header_dialogRequestId
                        if name == 'DeleteAlert' and 'dialogRequestId' in json.loads(value['response'])[index]['directive']['header']:
                                dialogRequestId = json.loads(value['response'])[index]['directive']['header']['dialogRequestId']
                                if len(str(dialogRequestId)) > 0:
                                    directiveSet.add('DeleteAlert_header_dialogRequestId')

                        # DeleteAlert_payload_token
                        if name == 'DeleteAlert' and 'payload' in json.loads(value['response'])[index]['directive']:
                            if 'token' in json.loads(value['response'])[index]['directive']['payload']:
                                token = json.loads(value['response'])[index]['directive']['payload']['token']
                                if len(str(token)) > 0:
                                    directiveSet.add('DeleteAlert_payload_token')

                        # 校验name和namespace是否一一对应
                        if name == 'HtmlView':
                            if namespace == 'ai.dueros.device_interface.screen':
                                cmd = namespace + '.' + name
                                directiveSet.add(cmd)
                            else:
                                print name + ' not correspond with ' + namespace

                        # HtmlView_header_messageId
                        if name == 'HtmlView' and 'messageId' in json.loads(value['request'])['event']['header']:
                            messageId = json.loads(value['request'])['event']['header']['messageId']
                            if len(str(messageId)) > 0:
                                directiveSet.add("HtmlView_header_messageId")

                        # HtmlView_payload_url
                        if name == 'HtmlView' and 'payload' in json.loads(value['request'])['event']['header']:
                            if 'url' in json.loads(value['request'])['event']['payload']:
                                url = json.loads(value['request'])['event']['payload']['url']
                                if type(url) == 'str' and url.startswith('http'):
                                    directiveSet.add("HtmlView_payload_url")

                        # HtmlView_payload_token
                        if name == 'HtmlView' and 'payload' in json.loads(value['request'])['event']['header']:
                            if 'token' in json.loads(value['request'])['event']['payload']:
                                token = json.loads(value['request'])['event']['payload']['token']
                                if type(token) == 'str' and len(token) > 0:
                                    directiveSet.add("HtmlView_payload_token")

                        # 输出不在开发平台上的指令
                        notContainDirFile = open('not_contain_directives.txt', 'a+')
                        if name not in name_list:
                            directive_str = json.dumps(json.loads(value['response'])[index]['directive']) + '\n' + '------------------------------'
                            print>>notContainDirFile, directive_str
                        notContainDirFile.close()

#                if 'directive' in json.loads(item):
#                    namespace = item['directive']['header']['namespace']
#                    name = item['directive']['header']['name']

            return directiveSet

    def getPingSet(self, eventDict):
        return self.getEventSet(eventDict)

    def getDirectiveDownloadChannelSet(self, directiveDict):
        return self.getDirectiveSet(directiveDict)
