#!/usr/bin/python
#coding:utf-8
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
from lib import ControlLog
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
import chardet
from nose_ittr import IttrMultiplier, ittr



def init_querylist():
    tmpdict = dict()
    with open("./querylist.txt", 'r') as fd:
        for line in fd.readlines():
            k, v = line.split()
            tmpdict[k.strip()] = v.strip()
    return tmpdict

controller = ControlLog.ControlLog()
deviceid = 'FF31F02122D428E2335E0261'
controller.setFilterDeviceid(deviceid)
controller.transLogFileDict("./lib/suning0302.log")
querydict = init_querylist()

eventSet = controller.getEventSet(controller.eventDict)
directiveSet = controller.getDirectiveSet(controller.directiveDict)
#directivedownloadchannelSet = controller.getDirectiveSet(controller.directivechannelDict)


class TestDCSCase(object):

    def getDirectiveDictSection(self, logid, logtime, tmpdict):
        logdcdict = dict()
        for i in range(logtime - 20000, logtime + 1000000, 1):
            if i in tmpdict.keys() and logid == tmpdict[i]['logid']:
                dc_logtime = i
                logdcdict[i] = tmpdict[i]
        return logdcdict

    def getEventDictSectionAfter(self, logtime, tmpdict):
        logeventdict = dict()
#        print type(logtime)#str
        for i in range(logtime - 20000, logtime + 990000, 1):
            if i in tmpdict.keys():
                logeventdict[i] = tmpdict[i]
        return logeventdict

    def getEventDictSectionBefore(self, logtime, tmpdict):
        logeventdict = dict()
        for i in range(logtime - 300000, logtime + 300000, 1):
            if i in tmpdict.keys():
                logeventdict[i] = tmpdict[i]
        return logeventdict

    def getEventDictSectionState(self, logtime, tmpdict):
        logeventdict = dict()
        for i in range(logtime - 20000, logtime + 3600000, 1):
            if i in tmpdict.keys():
                logeventdict[i] = tmpdict[i]
        return logeventdict

    def getEventDictSectionAfter_Longtime(self, logtime, tmpdict):
        logeventdict = dict()
#        for key, value in tmpdict.items():
#            if value.has_key('request'):
#                print json.loads(value['request'])['event']['header']['name']
#                namespace = json.loads(value['request'])['event']['header']['namespace']
#                name = json.loads(value['request'])['event']['header']['name']
#        print type(logtime)
        for i in range(logtime - 30000, logtime + 6000000, 1):
            if i in tmpdict.keys():
                logeventdict[i] = tmpdict[i]
        return logeventdict

    def getDialogRequestId(self, rorr):
        idSet = set()
        if isinstance(rorr, list):
            #response
            for item in rorr:
                if "directive" in item.keys() and "header" in item["directive"].keys():
                    dialogRequestId = item["directive"]["header"]["dialogRequestId"]
                    idSet.add(dialogRequestId)
            assert len(idSet) == 1
            return dialogRequestId
        elif isinstance(rorr, dict):
            # request
            if "event" in rorr.keys() and "header" in rorr["event"].keys():
                return rorr["event"]["header"]["dialogRequestId"]

    def getLogtimeToQuery(self, query):
        for key, value in controller.eventDict.items():
            if 'asr_text' in value.keys():
                songname = value['asr_text']
                if songname.find(query.strip()) != -1:
                    logtime = value['logtime']
                    return logtime
        return ""


# PlaybackState
    def checkStatePlaybackState(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        playbackState_cmd = event + "PlaybackState"
#        print controller.getEventSet(logeventdict)
        assert playbackState_cmd in controller.getEventSet(logeventdict) 

    def checkStatePlaybackStatePayloadToken(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        playbackState_cmd = event + "PlaybackState_payload_token"
        assert playbackState_cmd in controller.getEventSet(logeventdict) 

    def checkStatePlaybackStatePayloadOffsetInMilliseconds(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        playbackState_cmd = event + "PlaybackState_payload_offsetInMilliseconds"
        assert playbackState_cmd in controller.getEventSet(logeventdict) 

    def checkStatePlaybackStatePayloadPlayerActivity(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        playbackState_cmd = event + "PlaybackState_payload_playerActivity"
        assert playbackState_cmd in controller.getEventSet(logeventdict) 


# ViewState
    def checkStateViewState(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        viewState_cmd = event + "ViewState"
#        print controller.getEventSet(logeventdict)
        assert viewState_cmd in controller.getEventSet(logeventdict)

    def checkStateViewStatePayloadToken(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        viewState_cmd = event + "ViewState_payload_token"
#        print controller.getEventSet(logeventdict)
        assert viewState_cmd in controller.getEventSet(logeventdict)


# AlertsState
    def checkStateAlertsState(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

    def checkStateAlertsStatePayloadAllAlertsToken(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState_payload_allAlerts_token"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

    def checkStateAlertsStatePayloadAllAlertsType(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState_payload_allAlerts_type"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

    def checkStateAlertsStatePayloadAllAlertsScheduledTime(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState_payload_allAlerts_scheduledTime"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

    def checkStateAlertsStatePayloadActiveAlertsToken(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState_payload_activeAlerts_token"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

    def checkStateAlertsStatePayloadActiveAlertsType(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState_payload_activeAlerts_type"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

    def checkStateAlertsStatePayloadActiveAlertsScheduledTime(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        alertsState_cmd = event + "AlertsState_payload_activeAlerts_scheduledTime"
        assert alertsState_cmd in controller.getEventSet(logeventdict)

# VolumeState
    def checkStateVolumeState(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        speechState_cmd = event + "VolumeState"
        assert speechState_cmd in controller.getEventSet(logeventdict)

    def checkStateVolumeStatePayloadVolume(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        payloadVolume_cmd = event + "VolumeState_payload_volume"
        assert payloadVolume_cmd in controller.getEventSet(logeventdict)

    def checkStateVolumeStatePayloadMuted(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        payloadMuted_cmd = event + "VolumeState_payload_muted"
        assert payloadMuted_cmd in controller.getEventSet(logeventdict)


# SpeechState
    def checkStateSpeechState(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        speechState_cmd = event + "SpeechState"
        assert speechState_cmd in controller.getEventSet(logeventdict)

    def checkStateSpeechStatePayloadToken(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        payloadToken_cmd = event + "SpeechState_payload_token"
        assert payloadToken_cmd in controller.getEventSet(logeventdict)

    def checkStateSpeechStatePayloadOffsetInMilliseconds(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        offsetInMilliseconds_cmd = event +"SpeechState_payload_offsetInMilliseconds"
        assert offsetInMilliseconds_cmd in controller.getEventSet(logeventdict)

    def checkStateSpeechStatePayloadPlayerActivity(self, logtime, event):
        logeventdict = self.getEventDictSectionState(logtime, controller.eventDict)
        playerActivity_cmd = event + "SpeechState_payload_playerActivity"
        assert playerActivity_cmd in controller.getEventSet(logeventdict)


# ListenStarted
    def checkEventListenStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
#        print controller.getEventSet(logeventdict)
        listenSteartd_cmd = 'ai.dueros.device_interface.voice_input.ListenStarted'
#        if listenSteartd_cmd in controller.getEventSet(logeventdict):
#            print listenSteartd_cmd
#        elif 'SpeechRecognizer.ListenStarted' in controller.getEventSet(logeventdict):
#            print 'SpeechRecognizer.ListenStarted'
        assert listenSteartd_cmd in controller.getEventSet(logeventdict) or 'SpeechRecognizer.Recognize' in controller.getEventSet(logeventdict) 

    def checkListenStartedAndStopListen(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
#        print controller.getEventSet(logeventdict)
        listenSteartd_cmd = 'ai.dueros.device_interface.voice_input.ListenStarted'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
#        print controller.getDirectiveSet(logdcdict)
        stoplisten_cmd = 'ai.dueros.device_interface.voice_input.StopListen'
        if listenSteartd_cmd in controller.getEventSet(logeventdict) or 'SpeechRecognizer.Recognize' in controller.getEventSet(logeventdict):
            if stoplisten_cmd in controller.getDirectiveSet(logdcdict) or 'SpeechRecognizer.StopCapture' in controller.getDirectiveSet(logdcdict): 
                assert 'StartedAndStopListen' == 'StartedAndStopListen'
            else:
                assert 'StartedAndStopListen' == 'AndStopListen'

    def checkListenStartedAndSpeak(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        listenSteartd_cmd = 'ai.dueros.device_interface.voice_input.ListenStarted'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'ai.dueros.device_interface.voice_output.Speak'
        if listenSteartd_cmd in controller.getEventSet(logeventdict) or 'SpeechRecognizer.Recognize' in controller.getEventSet(logeventdict):
            if speak_cmd in controller.getEventSet(logeventdict) or 'SpeechRecognizer.Speak' in controller.getEventSet(logeventdict):
                assert 'StartedAndSpeak' == 'StartedAndSpeak'
            else:
                assert 'StartedAndSpeak' == 'StarAndSpeak'


    def checkEventListenStartedPayloadHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        listenSteartd_payloadFormat = 'ListenStarted_header_messageId'
        assert listenSteartd_payloadFormat in controller.getEventSet(logeventdict)

    def checkEventListenStartedPayloadHeaderDialogRequestId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        listenSteartd_payloadFormat = 'ListenStarted_header_dialogRequestId'
        assert listenSteartd_payloadFormat in controller.getEventSet(logeventdict)

    def checkEventListenStartedPayloadFormat(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        listenSteartd_payloadFormat = 'ListenStarted_payload_format'
        assert listenSteartd_payloadFormat in controller.getEventSet(logeventdict)



#StopListen
    def checkDirectiveStopListen(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        stoplisten_cmd = 'ai.dueros.device_interface.voice_input.StopListen'
        assert stoplisten_cmd in controller.getDirectiveSet(logdcdict) or 'SpeechRecognizer.StopCapture' in controller.getDirectiveSet(logdcdict)

    def checkDirectiveStopListenHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        stoplisten_cmd = 'StopListen_header_messageId'
        assert stoplisten_cmd in controller.getDirectiveSet(logdcdict)

    def checkDirectiveStopListenHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        stoplisten_cmd = 'StopListen_header_dialogRequestId'
        assert stoplisten_cmd in controller.getDirectiveSet(logdcdict)



#Listen
    def checkDirectiveListen(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
#        print controller.getDirectiveSet(logdcdict)
        listen_cmd = 'ai.dueros.device_interface.voice_input.Listen'
#        if listen_cmd in controller.getDirectiveSet(logdcdict):
#            print listen_cmd
#        elif 'SpeechRecognizer.ExpectSpeech' in controller.getDirectiveSet(logdcdict):
#            print 'SpeechRecognizer.ExpectSpeech'
        assert listen_cmd in controller.getDirectiveSet(logdcdict) or 'SpeechRecognizer.ExpectSpeech' in controller.getDirectiveSet(logdcdict)

    def checkDirectiveListenHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        listen_cmd = 'Listen_header_messageId'
        assert listen_cmd in controller.getDirectiveSet(logdcdict)

    def checkDirectiveListenHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        listen_cmd = 'Listen_header_dialogRequestId'
        assert listen_cmd in controller.getDirectiveSet(logdcdict)

    def checkDirectiveListenPayloadTimeoutInMilliseconds(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        listen_cmd = 'Listen_payload_timeoutInMilliseconds'
        assert listen_cmd in controller.getDirectiveSet(logdcdict)


#无ListenTimedOut

#Speak
    def checkDirectiveSpeak(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'ai.dueros.device_interface.voice_output.Speak'
        assert speak_cmd in controller.getDirectiveSet(logddict) or 'SpeechSynthesizer.Speak' in controller.getDirectiveSet(logddict)

    def checkSpeakAndSpeechStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        speak_cmd = 'ai.dueros.device_interface.voice_output.Speak'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speechStarted_cmd = 'ai.dueros.device_interface.voice_output.SpeechStarted'
        if speak_cmd in controller.getDirectiveSet(logdcdict) or 'SpeechRecognizer.Speak' in controller.getDirectiveSet(logdcdict): 
            if speechStarted_cmd in controller.getEventSet(logeventdict) or 'SpeechRecognizer.SpeechStarted' in controller.getEventSet(logeventdict):
                assert 'SpeakAndSpeechStarted' == 'SpeakAndSpeechStarted'

    def checkSpeakAndSpeechFinished(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        speak_cmd = 'ai.dueros.device_interface.voice_output.Speak'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speechFinished_cmd = 'ai.dueros.device_interface.voice_output.SpeechFinished'
        if speak_cmd in controller.getDirectiveSet(logdcdict) or 'SpeechRecognizer.Speak' in controller.getDirectiveSet(logdcdict): 
            if speechFinished_cmd in controller.getEventSet(logeventdict) or 'SpeechRecognizer.SpeechStarted' in controller.getEventSet(logeventdict):
                assert 'SpeakAndSpeechFinished' == 'SpeakAndSpeechFinished'
            else:
                assert 'SpeakAndSpeechFinished' == 'AndSpeechFinished'

    def checkDirectiveSpeakHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'Speak_header_messageId'
        assert speak_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSpeakHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'Speak_header_dialogRequestId'
        assert speak_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSpeakPayloadFormat(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'Speak_payload_format'
        assert speak_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSpeakPayloadToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'Speak_payload_token'
        assert speak_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSpeakPayloadUrl(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        speak_cmd = 'Speak_payload_url'
        assert speak_cmd in controller.getDirectiveSet(logddict)



#SpeechStarted
    def checkEventSpeechStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        speechStarted_cmd = "ai.dueros.device_interface.voice_output.SpeechStarted"
        assert speechStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventSpeechStartedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        SpeechStarted_header_messageId_cmd = "SpeechStarted_header_messageId"
        assert SpeechStarted_header_messageId_cmd in controller.getEventSet(logeventdict)

    def checkEventSpeechStartedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        SpeechStarted_payload_token_cmd = "SpeechStarted_payload_token"
        assert SpeechStarted_payload_token_cmd in controller.getEventSet(logeventdict)



#SpeechFinished
    def checkEventSpeechFinished(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        speechFinished_cmd = 'ai.dueros.device_interface.voice_output.SpeechFinished'
        assert speechFinished_cmd in controller.getEventSet(logeventdict) or 'SpeechSynthesizer.SpeechFinished' in controller.getEventSet(logeventdict)

    def checkEventSpeechFinishedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        speechFinished_cmd = "SpeechFinished_header_messageId"
        assert speechFinished_cmd in controller.getEventSet(logeventdict)

    def checkEventSpeechFinishedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        SpeechFinished_payload_token_cmd = "SpeechFinished_payload_token"
        assert SpeechFinished_payload_token_cmd in controller.getEventSet(logeventdict)



#SetVolume
    def checkDirectiveSetVolume(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        setVolume_cmd = 'ai.dueros.device_interface.speaker_controller.SetVolume'
        assert setVolume_cmd in controller.getDirectiveSet(logddict) or 'Speaker.SetVolume' in controller.getDirectiveSet(logddict)

    def checkSetVolumeAndVolumeChanged(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        setVolume_cmd = 'ai.dueros.device_interface.speaker_controller.SetVolume'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        volumeChanged_cmd = 'ai.dueros.device_interface.speaker_controller.VolumeChanged'
        if setVolume_cmd in controller.getDirectiveSet(logdcdict) or 'Speaker.VolumeChanged' in controller.getDirectiveSet(logdcdict): 
            if volumeChanged_cmd in controller.getEventSet(logeventdict) or 'Speaker.VolumeChanged' in controller.getEventSet(logeventdict):
                assert 'SetVolumeAndVolumeChanged' == 'SetVolumeAndVolumeChanged'
            else :
                assert 'SetVolumeAndVolumeChanged' == 'AndVolumeChanged'


    def checkDirectiveSetVolumeHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        setVolume_cmd = 'SetVolume_header_messageId'
        assert setVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetVolumeHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        setVolume_cmd = 'SetVolume_header_dialogRequestId'
        assert setVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetVolumePayloadVolume(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        setVolume_cmd = 'SetVolume_payload_volume'
        assert setVolume_cmd in controller.getDirectiveSet(logddict)



#AdjustVolume
    def checkDirectiveAdjustVolume(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'ai.dueros.device_interface.speaker_controller.AdjustVolume'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict) or 'Speaker.AdjustVolume' in controller.getDirectiveSet(logddict)

    def checkAdjustVolumeAndVolumeChanged(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        adjustVolume_cmd = 'ai.dueros.device_interface.speaker_controller.AdjustVolume'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        volumeChanged_cmd = 'ai.dueros.device_interface.speaker_controller.VolumeChanged'
        if adjustVolume_cmd in controller.getDirectiveSet(logdcdict) or 'Speaker.AdjustVolume' in controller.getDirectiveSet(logdcdict): 
            if volumeChanged_cmd in controller.getEventSet(logeventdict) or 'Speaker.VolumeChanged' in controller.getEventSet(logeventdict):
                assert 'SpeakAndSpeechStarted' == 'SpeakAndSpeechStarted'
            else:
                assert 'SpeakAndSpeechStarted' == 'AndSpeechStarted'

    def checkDirectiveAdjustVolumeHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'AdjustVolume_header_messageId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveAdjustVolumeHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'AdjustVolume_header_dialogRequestId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveAdjustVolumePayloadVolume(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'AdjustVolume_payload_volume'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)



#VolumeChanged
    def checkEventVolumeChanged(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "ai.dueros.device_interface.speaker_controller.VolumeChanged"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict) or 'Speaker.VolumeChanged' in controller.getEventSet(logeventdict)

    def checkEventVolumeChangedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "VolumeChanged_header_messageId"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict)

    def checkEventVolumeChangedPayloadVolume(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "VolumeChanged_payload_volume"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict)

    def checkEventVolumeChangedPayloadMuted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "VolumeChanged_payload_muted"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict)



#SetMute
    def checkDirectiveSetMute(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        setMute_cmd = 'ai.dueros.device_interface.speaker_controller.SetMute'
        assert setMute_cmd in controller.getDirectiveSet(logddict) or 'Speaker.SetMute' in controller.getDirectiveSet(logddict)

    def checkSetMuteAndMutedChanged(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        setMute_cmd = 'ai.dueros.device_interface.speaker_controller.SetMute'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        muteChanged_cmd = 'ai.dueros.device_interface.speaker_controller.MuteChanged'
        if setMute_cmd in controller.getDirectiveSet(logdcdict) or 'Speaker.SetMute' in controller.getDirectiveSet(logdcdict): 
            if muteChanged_cmd in controller.getEventSet(logeventdict) or 'Speaker.MuteChanged' in controller.getEventSet(logeventdict):
                assert 'SetMuteAndMutedChanged' == 'SetMuteAndMutedChanged'
            else:
                assert 'SetMuteAndMutedChanged' == 'AndMutedChanged'


    def checkDirectiveSetMuteHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetMute_header_messageId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetMuteHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetMute_header_dialogRequestId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetMutePayloadMute(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetMute_payload_mute'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)



#MuteChanged
    def checkEventMuteChanged(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        muteChanged_cmd = 'ai.dueros.device_interface.speaker_controller.MuteChanged'
        assert muteChanged_cmd in controller.getEventSet(logeventdict) or 'Speaker.MuteChanged' in controller.getEventSet(logeventdict)

    def checkEventMuteChangedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "MuteChanged_header_messageId"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict)

    def checkEventMuteChangedPayloadVolume(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "MuteChanged_payload_volume"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict)

    def checkEventMuteChangedPayloadMuted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        volumeChanged_cmd = "MuteChanged_payload_muted"
        assert volumeChanged_cmd in controller.getEventSet(logeventdict)



#Play
    def checkDirectivePlay(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'ai.dueros.device_interface.audio_player.Play'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkPlayProgressReportDelayInMillisecondsProgressReportDelayElapsed(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        play_cmd = 'Play_payload_audioItem_stream_progressReport_progressReportDelayInMilliseconds'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        progress_cmd = 'ai.dueros.device_interface.audio_player.ProgressReportDelayElapsed'
        if play_cmd in controller.getDirectiveSet(logeventdict):
            if progress_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.ProgressReportDelayElapsed' in controller.getEventSet(logeventdict):
                assert 'PlayProgressReportDelayInMillisecondsProgressReportDelayElapsed' == 'PlayProgressReportDelayInMillisecondsProgressReportDelayElapsed'
            else:
                assert 'PlayProgressReportDelayInMillisecondsProgressReportDelayElapsed' == 'ProgressReportDelayInMillisecondsProgressReportDelayElapsed'

    def checkPlayProgressReportIntervalInMillisecondsProgressReportIntervalElapsed(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        play_cmd = 'Play_payload_audioItem_stream_progressReport_progressReportIntervalInMilliseconds'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        progress_cmd = 'ai.dueros.device_interface.audio_player.ProgressReportIntervalElapsed'
        if play_cmd in controller.getDirectiveSet(logeventdict):
            if progress_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.ProgressReportIntervalElapsed' in controller.getEventSet(logeventdict):
                assert 'PlayProgressReportIntervalInMillisecondsProgressReportIntervalElapsed' == 'PlayProgressReportIntervalInMillisecondsProgressReportIntervalElapsed'
            else:
                assert 'PlayProgressReportIntervalInMillisecondsProgressReportIntervalElapsed' == 'ProgressReportIntervalInMillisecondsProgressReportIntervalElapsed'

    def checkDirectivePlayHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_header_messageId'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_header_dialogRequestId'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadPlayBehaviorENQUEUEExpectedPreviousToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_playBehavior_ENQUEUE_expectedPreviousToken'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadPlayBehaviorREPLACEENQUEUEDExpectedPreviousToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_playBehavior_REPLACE_ENQUEUED_expectedPreviousToken'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadPlayBehaviorREPLACEALL(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_playBehavior_REPLACE_ALL'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)


    def checkPlayBehaviorREPLACE_ALLPlaybackStopped(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        play_cmd = "Play_payload_playBehavior_REPLACE_ALL"
        playbackStopped_cmd = "ai.dueros.device_interface.audio_player.PlaybackStopped"
        if play_cmd in controller.getEventSet(logeventdict) :
            if playbackStopped_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStopped' in controller.getEventSet(logeventdict):
                assert 'PlayBehaviorREPLACE_ALLPlaybackStopped' == 'PlayBehaviorREPLACE_ALLPlaybackStopped' 
            else:
                assert 'PlayBehaviorREPLACE_ALLPlaybackStopped' == 'BehaviorREPLACE_ALLPlaybackStopped'

    def checkDirectivePlayPayloadAudioItemAudioItemId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_audioItemId'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadAudioItemStream_url(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_url'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadAudioItemStreamStreamFormat(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_streamFormat'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadAudioItemStreamOffsetInMilliseconds(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_offsetInMilliseconds'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadAudioItemStreamExpiryTime(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_expiryTime'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadAudioItemStreamProgressReportProgressReportDelayInMilliseconds(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_progressReport_progressReportDelayInMilliseconds'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayPayloadAudioItemStreamProgressReportProgressReportIntervalInMilliseconds(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_progressReport_progressReportIntervalInMilliseconds'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayAudioItemStreamToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_token'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkDirectivePlayAudioItemStreamTokenExpectedPreviousToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        play_cmd = 'Play_payload_audioItem_stream_expectedPreviousToken'
        assert play_cmd in controller.getDirectiveSet(logeventdict) or 'AudioPlayer.Play' in controller.getDirectiveSet(logeventdict)

    def checkClearQueuePlaybackQueueCleared (self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        clear_cmd = "ai.dueros.device_interface.audio_player.ClearQueue"
        playback_cmd = "ai.dueros.device_interface.audio_player.PlaybackQueueCleared"
        if clear_cmd in controller.getEventSet(logeventdict):
            if playback_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackQueueCleared' in controller.getEventSet(logeventdict):
                assert 'ClearQueuePlaybackQueueCleared' == 'ClearQueuePlaybackQueueCleared' 
            else:
                assert 'ClearQueuePlaybackQueueCleared' == 'QueuePlaybackQueueCleared'





#PlaybackStarted
    def checkEventPlaybackStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "ai.dueros.device_interface.audio_player.PlaybackStarted"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStarted' in controller.getEventSet(logeventdict)

    def checkPlaybackStartedPlaybackStutterStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "ai.dueros.device_interface.audio_player.PlaybackStarted"
        PlaybackStutterStarted_cmd = "ai.dueros.device_interface.audio_player.PlaybackStutterStarted"
        if playbackStarted_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStarted' in controller.getEventSet(logeventdict):
            if PlaybackStutterStarted_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStutterStarted' in controller.getEventSet(logeventdict):
                assert 'PlaybackStartedPlaybackStutterStarted' == 'PlaybackStartedPlaybackStutterStarted' 
            else:
                assert 'PlaybackStartedPlaybackStutterStarted' == 'backStartedPlaybackStutterStarted'

    def checkPlaybackStutterStartedPlaybackStutterFinished(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "ai.dueros.device_interface.audio_player.PlaybackStutterStarted"
        PlaybackStutterStarted_cmd = "ai.dueros.device_interface.audio_player.PlaybackStutterFinished"
        if playbackStarted_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStutterStarted' in controller.getEventSet(logeventdict):
            if PlaybackStutterStarted_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStutterStarted' in controller.getEventSet(logeventdict):
                assert 'PlaybackStutterStartedPlaybackStutterFinished' == 'PlaybackStutterStartedPlaybackStutterFinished' 
            else:
                assert 'PlaybackStutterStartedPlaybackStutterFinished' == 'StutterStartedPlaybackStutterFinished'

    def checkEventPlaybackStartedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "PlaybackStarted_header_messageId"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStartedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "PlaybackStarted_payload_token"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStartedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "PlaybackStarted_payload_offsetInMilliseconds"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict)



#PlaybackFinished
    def checkEventPlaybackFinished(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackFinished_cmd = "ai.dueros.device_interface.audio_player.PlaybackFinished"
        assert playbackFinished_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackFinished' in controller.getEventSet(logeventdict)

    def checkEventPlaybackFinishedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "PlaybackFinished_header_messageId"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackFinishedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "PlaybackFinished_payload_token"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackFinishedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStarted_cmd = "PlaybackFinished_payload_offsetInMilliseconds"
        assert playbackStarted_cmd in controller.getEventSet(logeventdict)



#PlaybackNearlyFinished
    def checkEventPlaybackNearlyFinished(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackNearlyFinished_cmd = "ai.dueros.device_interface.audio_player.PlaybackNearlyFinished"
        assert playbackNearlyFinished_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackNearlyFinished' in controller.getEventSet(logeventdict)

    def checkEventPlaybackNearlyFinishedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackNearlyFinished_cmd = "PlaybackNearlyFinished_header_messageId"
        assert playbackNearlyFinished_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackNearlyFinishedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackNearlyFinished_cmd = "PlaybackNearlyFinished_payload_token"
        assert playbackNearlyFinished_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackNearlyFinishedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackNearlyFinished_cmd = "PlaybackNearlyFinished_payload_offsetInMilliseconds"
        assert playbackNearlyFinished_cmd in controller.getEventSet(logeventdict)


#无PlaybackFailed
#ProgressReportDelayElapsed
    def checkEventProgressReportDelayElapsed(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ai.dueros.device_interface.audio_player.ProgressReportDelayElapsed"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.ProgressReportDelayElapsed' in controller.getEventSet(logeventdict)

    def checkEventProgressReportDelayElapsedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ProgressReportDelayElapsed_header_messageId"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict)

    def checkEventProgressReportDelayElapsedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ProgressReportDelayElapsed_payload_token"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict)

    def checkEventProgressReportDelayElapsedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ProgressReportDelayElapsed_payload_offsetInMilliseconds"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict)


#ProgressReportIntervalElapsed
    def checkEventProgressReportIntervalElapsed(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportIntervalElapsed_cmd = "ai.dueros.device_interface.audio_player.ProgressReportIntervalElapsed"
        assert progressReportIntervalElapsed_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.ProgressReportIntervalElapsed' in controller.getEventSet(logeventdict)

    def checkEventProgressReportIntervalElapsedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ProgressReportIntervalElapsed_header_messageId"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict)

    def checkEventProgressReportIntervalElapsedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ProgressReportIntervalElapsed_payload_token"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict)

    def checkEventProgressReportIntervalElapsedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        progressReportDelayElapsed_cmd = "ProgressReportIntervalElapsed_payload_offsetInMilliseconds"
        assert progressReportDelayElapsed_cmd in controller.getEventSet(logeventdict)



#Stop
    def checkDirectiveStop(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        stop_cmd = 'ai.dueros.device_interface.audio_player.Stop'
        assert stop_cmd in controller.getDirectiveSet(logddict) or 'AudioPlayer.Stop' in controller.getDirectiveSet(logddict)

    def checkStopPlaybackStopped(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        stop_cmd = 'ai.dueros.device_interface.audio_player.Stop'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        playbackStopped_cmd = 'ai.dueros.device_interface.audio_player.PlaybackStopped'
        if stop_cmd in controller.getDirectiveSet(logdcdict) or 'AudioPlayer.Stop' in controller.getDirectiveSet(logdcdict): 
            if playbackStopped_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStopped' in controller.getEventSet(logeventdict):
                assert 'StopPlaybackStopped' == 'StopPlaybackStopped'
            else:
                assert 'StopPlaybackStopped' == 'PlaybackStopped'

    def checkDirectiveStopHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'Stop_header_messageId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveStopHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'Stop_header_dialogRequestId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)



#PlaybackStutterStarted
    def checkEventPlaybackStutterStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStutterStarted_cmd = "ai.dueros.device_interface.audio_player.PlaybackStutterStarted"
        assert playbackStutterStarted_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStutterStarted' in controller.getEventSet(logeventdict)

    def checkEventPlaybackStutterStartedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        PlaybackStutterStarted_cmd = "PlaybackStutterStarted_header_messageId"
        assert PlaybackStutterStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStutterStartedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        PlaybackStutterStarted_cmd = "PlaybackStutterStarted_payload_token"
        assert PlaybackStutterStarted_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStutterStartedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        PlaybackStutterStarted_cmd = "PlaybackStutterStarted_payload_offsetInMilliseconds"
        assert PlaybackStutterStarted_cmd in controller.getEventSet(logeventdict)



#PlaybackStutterFinished
    def checkEventPlaybackStutterFinished(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStutterFinished_cmd = "ai.dueros.device_interface.audio_player.PlaybackStutterFinished"
        assert playbackStutterFinished_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStutterFinished' in controller.getEventSet(logeventdict)

    def checkEventPlaybackStutterFinishedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStutterFinished_cmd = "PlaybackStutterFinished_header_messageId"
        assert playbackStutterFinished_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStutterFinishedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStutterFinished_cmd = "PlaybackStutterFinished_payload_token"
        assert playbackStutterFinished_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStutterFinishedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStutterFinished_cmd = "PlaybackStutterFinished_payload_offsetInMilliseconds"
        assert playbackStutterFinished_cmd in controller.getEventSet(logeventdict)



#PlaybackStopped
    def checkEventPlaybackStopped(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStopped_cmd = "ai.dueros.device_interface.audio_player.PlaybackStopped"
        assert playbackStopped_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackStopped' in controller.getEventSet(logeventdict)

    def checkEventPlaybackStoppedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStopped_cmd = "PlaybackStopped_header_messageId"
        assert playbackStopped_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStoppedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStopped_cmd = "PlaybackStopped_payload_token"
        assert playbackStopped_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackStoppeddPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackStopped_cmd = "PlaybackStopped_payload_offsetInMilliseconds"
        assert playbackStopped_cmd in controller.getEventSet(logeventdict)



#PlaybackPaused
    def checkEventPlaybackPaused(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackPaused_cmd = "ai.dueros.device_interface.audio_player.PlaybackPaused"
        assert playbackPaused_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackPaused' in controller.getEventSet(logeventdict)

    def checkPlaybackPausedPlaybackResumed(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        play_cmd = "ai.dueros.device_interface.audio_player.PlaybackPaused"
        Playback_cmd = "ai.dueros.device_interface.audio_player.PlaybackResumed"
        if play_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackPaused' in controller.getEventSet(logeventdict):
            if Playback_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackResumed' in controller.getEventSet(logeventdict):
                assert 'PlaybackPausedPlaybackResumed' == 'PlaybackPausedPlaybackResumed' 
            else:
                assert 'PlaybackPausedPlaybackResumed' == 'backPausedPlaybackResumed'



    def checkEventPlaybackPausedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackPaused_cmd = "PlaybackPaused_header_messageId"
        assert playbackPaused_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackPausedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackPaused_cmd = "PlaybackPaused_payload_token"
        assert playbackPaused_cmd in controller.getEventSet(logeventdict)


    def checkEventPlaybackPausedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackPaused_cmd = "PlaybackPaused_payload_offsetInMilliseconds"
        assert playbackPaused_cmd in controller.getEventSet(logeventdict)



#PlaybackResumed
    def checkEventPlaybackResumed(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackResumed_cmd = "ai.dueros.device_interface.audio_player.PlaybackResumed"
        assert playbackResumed_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlaybackResumed' in controller.getEventSet(logeventdict)

    def checkEventPlaybackResumedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackResumed_cmd = "PlaybackResumed_header_messageId"
        assert playbackResumed_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackResumedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackResumed_cmd = "PlaybackResumed_payload_token"
        assert playbackResumed_cmd in controller.getEventSet(logeventdict)

    def checkEventPlaybackResumedPayloadOffsetInMilliseconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackResumed_cmd = "PlaybackResumed_payload_offsetInMilliseconds"
        assert playbackResumed_cmd in controller.getEventSet(logeventdict)

#无ClearQueue
#无PlaybackQueueCleared
#无StreamMetadataExtracted


#PlayCommandIssued
    def checkEventPlayCommandIssued(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.eventDict)
        playCommandIssued_cmd = "ai.dueros.device_interface.playback_controller.PlayCommandIssued"
        assert playCommandIssued_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PlayCommandIssued' in controller.getEventSet(logeventdict)

    def checkEventPlayCommandIssuedHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.eventDict)
        playCommandIssued_cmd = 'PlayCommandIssued_header_messageId'
        assert playCommandIssued_cmd in controller.getDirectiveSet(logddict)

#PauseCommandIssued
    def checkEventPauseCommandIssued(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        pauseCommandIssued_cmd = "ai.dueros.device_interface.playback_controller.PauseCommandIssued"
        assert pauseCommandIssued_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PauseCommandIssued' in controller.getEventSet(logeventdict)

    def checkEventPauseCommandIssuedHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.eventDict)
        PauseCommandIssued_cmd = 'PauseCommandIssued_header_messageId'
        assert PauseCommandIssued_cmd in controller.getDirectiveSet(logddict)

#NextCommandIssued
    def checkEventNextCommandIssued(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        nextCommandIssued_cmd = "ai.dueros.device_interface.playback_controller.NextCommandIssued"
        assert nextCommandIssued_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.NextCommandIssued' in controller.getEventSet(logeventdict)

    def checkEventNextCommandIssuedHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.eventDict)
        NextCommandIssued_cmd = 'NextCommandIssued_header_messageId'
        assert NextCommandIssued_cmd in controller.getDirectiveSet(logddict)

#PreviousCommandIssued
    def checkEventPreviousCommandIssued(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        previousCommandIssued_cmd = "ai.dueros.device_interface.playback_controller.PreviousCommandIssued"
        assert previousCommandIssued_cmd in controller.getEventSet(logeventdict) or 'AudioPlayer.PreviousCommandIssued' in controller.getEventSet(logeventdict)

    def checkEventPreviousCommandIssuedHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logeventdict = self.getDirectiveDictSection(logid, logtime, controller.eventDict)
        PreviousCommandIssued_cmd = 'PreviousCommandIssued_header_messageId'
        assert PreviousCommandIssued_cmd in controller.getDirectiveSet(logddict)



#SetAlert
    def checkDirectiveSetAlert(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        setAlert_cmd = 'ai.dueros.device_interface.alerts.SetAlert'
        assert setAlert_cmd in controller.getDirectiveSet(logddict) or 'Alerts.SetAlert' in controller.getDirectiveSet(logddict)

    def checkSetAlertSetAlertSucceeded(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        set_cmd = 'ai.dueros.device_interface.alerts.SetAlert'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        success_cmd = 'ai.dueros.device_interface.alerts.SetAlertSucceeded'
        if set_cmd in controller.getDirectiveSet(logdcdict) or 'Alerts.SetAlert' in controller.getDirectiveSet(logdcdict): 
            if success_cmd in controller.getEventSet(logeventdict) or 'Alerts.SetAlertSucceeded' in controller.getEventSet(logeventdict):
                assert 'SetAlertSetAlertSucceeded' == 'SetAlertSetAlertSucceeded'
            else:
                assert 'SetAlertSetAlertSucceeded' == 'AlertSetAlertSucceeded'


    def checkDirectiveSetAlertHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetAlert_header_messageId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetAlertHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetAlert_header_dialogRequestId'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetAlertPayloadToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetAlert_payload_token'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetAlertPayloadType(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetAlert_payload_type'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveSetAlertPayloadScheduledTime(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        adjustVolume_cmd = 'SetAlert_payload_scheduledTime'
        assert adjustVolume_cmd in controller.getDirectiveSet(logddict)

#SetAlertSucceeded
    def checkEventSetAlertSucceeded(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        setAlertSucceeded_cmd = 'ai.dueros.device_interface.alerts.SetAlertSucceeded'
        assert setAlertSucceeded_cmd in controller.getEventSet(logeventdict) or 'Alerts.SetAlertSucceeded' in controller.getEventSet(logeventdict)

    def checkEventSetAlertSucceededHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackResumed_cmd = "SetAlertSucceeded_header_messageId"
        assert playbackResumed_cmd in controller.getEventSet(logeventdict)

    def checkEventSetAlertSucceededPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        playbackResumed_cmd = "SetAlertSucceeded_payload_token"
        assert playbackResumed_cmd in controller.getEventSet(logeventdict)


#无SetAlertFailed

#DeleteAlert
    def checkDirectiveDeleteAlert(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        deleteAlert_cmd = 'ai.dueros.device_interface.alerts.DeleteAlert'
        assert deleteAlert_cmd in controller.getDirectiveSet(logddict) or 'Alerts.DeleteAlert' in controller.getDirectiveSet(logddict)


    def checkDeleteAlertDeleteAlertSucceeded(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        set_cmd = 'ai.dueros.device_interface.alerts.DeleteAlert'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        success_cmd = 'ai.dueros.device_interface.alerts.DeleteAlertSucceeded'
        if set_cmd in controller.getDirectiveSet(logdcdict) or 'Alerts.DeleteAlert' in controller.getDirectiveSet(logdcdict): 
            if success_cmd in controller.getEventSet(logeventdict) or 'Alerts.DeleteAlertSucceeded' in controller.getEventSet(logeventdict):
                assert 'DeleteAlertDeleteAlertSucceeded' == 'DeleteAlertDeleteAlertSucceeded'
            else:
                assert 'DeleteAlertDeleteAlertSucceeded' == 'AlertDeleteAlertSucceeded'

    def checkDeleteAlertAlertStopped(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        set_cmd = 'ai.dueros.device_interface.alerts.DeleteAlert'
        logid = controller.eventDict[logtime]['logid']
        logdcdict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        success_cmd = 'ai.dueros.device_interface.alerts.AlertStopped'
        if set_cmd in controller.getDirectiveSet(logdcdict) or 'Alerts.DeleteAlert' in controller.getDirectiveSet(logdcdict): 
            if success_cmd in controller.getEventSet(logeventdict) or 'Alerts.AlertStopped' in controller.getEventSet(logeventdict):
                assert 'DeleteAlertAlertStopped' == 'DeleteAlertAlertStopped'
            else:
                assert 'DeleteAlertAlertStopped' == 'AlertAlertStopped'


    def checkDirectiveDeleteAlertHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        deleteAlert_cmd = 'DeleteAlert_header_messageId'
        assert deleteAlert_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveDeleteAlertHeaderDialogRequestId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        deleteAlert_cmd = 'DeleteAlert_header_dialogRequestId'
        assert deleteAlert_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveDeleteAlertPayloadToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        deleteAlert_cmd = 'DeleteAlert_payload_token'
        assert deleteAlert_cmd in controller.getDirectiveSet(logddict)



#DeleteAlertSucceeded
    def checkEventDeleteAlertSucceeded(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        deleteAlertSucceeded_cmd = 'ai.dueros.device_interface.alerts.DeleteAlertSucceeded'
        assert deleteAlertSucceeded_cmd in controller.getEventSet(logeventdict) or 'Alerts.DeleteAlertSucceeded' in controller.getEventSet(logeventdict)

    def checkEventDeleteAlertSucceededHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        deleteAlertSucceeded_cmd = "DeleteAlertSucceeded_header_messageId"
        assert deleteAlertSucceeded_cmd in controller.getEventSet(logeventdict)

    def checkEventDeleteAlertSucceededPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        deleteAlertSucceeded_cmd = "DeleteAlertSucceeded_payload_token"
        assert deleteAlertSucceeded_cmd in controller.getEventSet(logeventdict)


#无DeleteAlertFailed    

#AlertStarted
    def checkEventAlertStarted(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertStarted_cmd = 'ai.dueros.device_interface.alerts.AlertStarted'
        assert alertStarted_cmd in controller.getEventSet(logeventdict) or 'Alerts.AlertStarted' in controller.getEventSet(logeventdict)

    def checkEventAlertStartedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        deleteAlertSucceeded_cmd = "AlertStarted_header_messageId"
        assert deleteAlertSucceeded_cmd in controller.getEventSet(logeventdict)

    def checkEventAlertStartedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        deleteAlertSucceeded_cmd = "AlertStarted_payload_token"
        assert deleteAlertSucceeded_cmd in controller.getEventSet(logeventdict)



#AlertStopped
    def checkEventAlertStopped(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertStopped_cmd = 'ai.dueros.device_interface.alerts.AlertStopped'
        assert alertStopped_cmd in controller.getEventSet(logeventdict) or 'Alerts.AlertStopped' in controller.getEventSet(logeventdict)

    def checkEventAlertStoppedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        AlertStopped_cmd = "AlertStopped_header_messageId"
        assert AlertStopped_cmd in controller.getEventSet(logeventdict)

    def checkEventAlertStoppedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertStopped_cmd = 'AlertStopped_payload_token'
        assert alertStopped_cmd in controller.getEventSet(logeventdict)



#AlertEnteredForeground
    def checkEventAlertEnteredForeground(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertEnteredForeground_cmd = 'ai.dueros.device_interface.alerts.AlertEnteredForeground'
        assert alertEnteredForeground_cmd in controller.getEventSet(logeventdict) or 'Alerts.AlertEnteredForeground' in controller.getEventSet(logeventdict)

    def checkEventAlertEnteredForegroundHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        AlertEnteredForeground_cmd = "AlertEnteredForeground_header_messageId"
        assert AlertEnteredForeground_cmd in controller.getEventSet(logeventdict)

    def checkEventAlertEnteredForegroundPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertStopped_cmd = 'AlertEnteredForeground_payload_token'

        assert alertStopped_cmd in controller.getEventSet(logeventdict)



#AlertEnteredBackground
    def checkEventAlertEnteredBackground(self, logtime): 
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertEnteredBackground_cmd = 'ai.dueros.device_interface.alerts.AlertEnteredBackground'
        assert alertEnteredBackground_cmd in controller.getDirectiveSet(logeventdict) or 'Alerts.AlertEnteredBackground' in controller.getEventSet(logeventdict)

    def checkEventAlertEnteredBackgroundHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        AlertEnteredBackground_cmd = "AlertEnteredBackground_header_messageId"
        assert AlertEnteredBackground_cmd in controller.getEventSet(logeventdict)

    def checkEventAlertEnteredBackgroundPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        alertStopped_cmd = 'AlertEnteredBackground_payload_token'
        assert alertStopped_cmd in controller.getEventSet(logeventdict)


#屏幕展示
#HtmlView
    def checkDirectiveHtmlView(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        HtmlView_cmd = 'ai.dueros.device_interface.screen.HtmlView'
        assert HtmlView_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveHtmlViewHeaderMessageId(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        HtmlView_cmd = 'HtmlView_header_messageId'
        assert HtmlView_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveHtmlViewPayloadUrl(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        HtmlView_cmd = 'HtmlView_payload_url'
        assert HtmlView_cmd in controller.getDirectiveSet(logddict)

    def checkDirectiveHtmlViewPayloadToken(self, logtime):
        logid = controller.eventDict[logtime]['logid']
        logddict = self.getDirectiveDictSection(logid, logtime, controller.directiveDict)
        HtmlView_cmd = 'HtmlView_payload_token'
        assert HtmlView_cmd in controller.getDirectiveSet(logddict)


 #LinkClicked
    def checkEventLinkClicked(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        LinkClicked_cmd = 'ai.dueros.device_interface.screen.LinkClicked'
        assert LinkClicked_cmd in controller.getEventSet(logddict)

    def checkEventLinkClickedHeaderMessageId(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        LinkClicked_cmd = 'LinkClicked_header_messageId'
        assert LinkClicked_cmd in controller.getEventSet(logddict)

    def checkEventLinkClickedPayloadUrl(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        LinkClicked_cmd = 'LinkClicked_payload_url'
        assert LinkClicked_cmd in controller.getEventSet(logddict)

    def checkEventLinkClickedPayloadToken(self, logtime):
        logeventdict = self.getEventDictSectionAfter(logtime, controller.eventDict)
        LinkClicked_cmd = 'LinkClicked_payload_token'
        assert LinkClicked_cmd in controller.getEventSet(logddict)


    #SynchronizeState
    def checkEventSynchronizeState(self, logtime):
        logeventdict = self.getEventDictSectionBefore(logtime, controller.eventDict)
        synchronizeState_cmd = 'ai.dueros.device_interface.system.SynchronizeState'
        assert synchronizeState_cmd in controller.getEventSet(logeventdict)  or 'System.SynchronizeState' in controller.getEventSet(logeventdict)



#UserInactivityReport
    def checkEventUserInactivityReport(self, logtime):
        logeventdict = self.getEventDictSectionAfter_Longtime(logtime, controller.eventDict)

        userInactivityReport_cmd = "UserInactivityReport"
        assert userInactivityReport_cmd in controller.getEventSet(logeventdict) or 'System.UserInactivityReport' in controller.getEventSet(logeventdict)

    def checkEventUserInactivityReportPayloadInactiveTimeInSeconds(self, logtime):
        logeventdict = self.getEventDictSectionAfter_Longtime(logtime, controller.eventDict)
        userInactivityReport_cmd = "UserInactivityReport_payload_inactiveTimeInSeconds"
        assert userInactivityReport_cmd in controller.getEventSet(logeventdict)

# ExceptionEncountered
    def checkEventExceptionEncountered(self, logtime):
        logeventdict = self.getEventDictSectionAfter_Longtime(logtime + 8500000, controller.eventDict)
        exceptionEncountered_cmd = "ai.dueros.device_interface.system.ExceptionEncountered"
        assert exceptionEncountered_cmd in controller.getDirectiveSet(logeventdict) or 'System.ExceptionEncountered' in controller.getDirectiveSet(logeventdict)

    def checkEventExceptionEncounteredPayloadUnparsedDirective(self, logtime):
        logeventdict = self.getEventDictSectionAfter_Longtime(logtime + 8500000, controller.eventDict)
        exceptionEncountered_cmd = "ExceptionEncountered_payload_unparsedDirective"
        assert exceptionEncountered_cmd in controller.getDirectiveSet(logeventdict)

    def checkEventExceptionEncounteredPayloadErrorType(self, logtime):
        logeventdict = self.getEventDictSectionAfter_Longtime(logtime + 8500000, controller.eventDict)
        exceptionEncountered_cmd = "ExceptionEncountered_payload_error_type"
        assert exceptionEncountered_cmd in controller.getDirectiveSet(logeventdict)

    def checkEventExceptionEncounteredPayloadErrorMessage(self, logtime):
        logeventdict = self.getEventDictSectionAfter_Longtime(logtime + 8500000, controller.eventDict)
        exceptionEncountered_cmd = "ExceptionEncountered_payload_error_message"
        assert exceptionEncountered_cmd in controller.getDirectiveSet(logeventdict)



# 测试case:


'''



#SynchronizeState_PlaybackState
    def test_state_SynchronizeState_PlaybackState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackState(logtime, "SynchronizeState")

    def test_state_SynchronizeState_PlaybackState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadToken(logtime, "SynchronizeState")

    def test_state_SynchronizeState_PlaybackState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadOffsetInMilliseconds(logtime, "SynchronizeState")

    def test_state_SynchronizeState_PlaybackState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadPlayerActivity(logtime, "SynchronizeState")


#SynchronizeState_ViewState
    def test_state_SynchronizeState_ViewState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewState(logtime, "SynchronizeState")

    def test_state_SynchronizeState_ViewState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewStatePayloadToken(logtime, "SynchronizeState")



#SynchronizeState_AlertsState
    def test_state_SynchronizeState_AlertsState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsState(logtime, "SynchronizeState")

    def test_state_SynchronizeState_AlertsState_payload_allAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsToken(logtime, "SynchronizeState")

    def test_state_SynchronizeState_AlertsState_payload_allAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsType(logtime, "SynchronizeState")

    def test_state_SynchronizeState_AlertsState_payload_allAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsScheduledTime(logtime, "SynchronizeState")

    def test_state_SynchronizeState_AlertsState_payload_activeAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsToken(logtime, "SynchronizeState")

    def test_state_SynchronizeState_AlertsState_payload_activeAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsType(logtime, "SynchronizeState")

    def test_state_SynchronizeState_AlertsState_payload_activeAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsScheduledTime(logtime, "SynchronizeState")



#SynchronizeState_VolumeState
    def test_state_SynchronizeState_VolumeState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeState(logtime, "SynchronizeState")

    def test_state__SynchronizeState_VolumeState_payload_volume(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadVolume(logtime, "SynchronizeState")

    def test_state__SynchronizeStatea_VolumeState_payload_muted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadMuted(logtime, "SynchronizeState")



#SynchronizeState_SpeechState
    def test_state_SynchronizeState_SpeechState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechState(logtime, "SynchronizeState")

    def test_state_SynchronizeState_SpeechState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadToken(logtime, "SynchronizeState")

    def test_state_SynchronizeState_SpeechState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadOffsetInMilliseconds(logtime, "SynchronizeState")

    def test_state_SynchronizeState_SpeechState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadPlayerActivity(logtime, "SynchronizeState")




#ListenStarted_PlaybackState
    def test_state_ListenStarted_PlaybackState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackState(logtime, "ListenStarted")

    def test_state_ListenStarted_PlaybackState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadToken(logtime, "ListenStarted")

    def test_state_ListenStarted_PlaybackState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadOffsetInMilliseconds(logtime, "ListenStarted")

    def test_state_ListenStarted_PlaybackState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadPlayerActivity(logtime, "ListenStarted")


#ListenStarted_ViewState
    def test_state_ListenStarted_ViewState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewState(logtime, "ListenStarted")

    def test_state_ListenStarted_ViewState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewStatePayloadToken(logtime, "ListenStarted")



#ListenStarted_AlertsState
    def test_state_ListenStarted_AlertsState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsState(logtime, "ListenStarted")

    def test_state_ListenStarted_AlertsState_payload_allAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsToken(logtime, "ListenStarted")

    def test_state_ListenStarted_AlertsState_payload_allAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsType(logtime, "ListenStarted")

    def test_state_ListenStarted_AlertsState_payload_allAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsScheduledTime(logtime, "ListenStarted")

    def test_state_ListenStarted_AlertsState_payload_activeAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsToken(logtime, "ListenStarted")

    def test_state_ListenStarted_AlertsState_payload_activeAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsType(logtime, "ListenStarted")

    def test_state_ListenStarted_AlertsState_payload_activeAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsScheduledTime(logtime, "ListenStarted")



#ListenStarted_VolumeState
    def test_state_ListenStarted_VolumeState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeState(logtime, "ListenStarted")

    def test_state__ListenStarted_VolumeState_payload_volume(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadVolume(logtime, "ListenStarted")

    def test_state__ListenStarteda_VolumeState_payload_muted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadMuted(logtime, "ListenStarted")



#ListenStarted_SpeechState
    def test_state_ListenStarted_SpeechState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechState(logtime, "ListenStarted")

    def test_state_ListenStarted_SpeechState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadToken(logtime, "ListenStarted")

    def test_state_ListenStarted_SpeechState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadOffsetInMilliseconds(logtime, "ListenStarted")

    def test_state_ListenStarted_SpeechState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadPlayerActivity(logtime, "ListenStarted")



#PlayCommandIssued_PlaybackState
    def test_state_PlayCommandIssued_PlaybackState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackState(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_PlaybackState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadToken(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_PlaybackState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadOffsetInMilliseconds(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_PlaybackState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadPlayerActivity(logtime, "PlayCommandIssued")


#PlayCommandIssued_ViewState
    def test_state_PlayCommandIssued_ViewState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewState(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_ViewState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewStatePayloadToken(logtime, "PlayCommandIssued")



#PlayCommandIssued_AlertsState
    def test_state_PlayCommandIssued_AlertsState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsState(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_AlertsState_payload_allAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsToken(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_AlertsState_payload_allAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsType(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_AlertsState_payload_allAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsScheduledTime(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_AlertsState_payload_activeAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsToken(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_AlertsState_payload_activeAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsType(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_AlertsState_payload_activeAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsScheduledTime(logtime, "PlayCommandIssued")



#PlayCommandIssued_VolumeState
    def test_state_PlayCommandIssued_VolumeState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeState(logtime, "PlayCommandIssued")

    def test_state__PlayCommandIssued_VolumeState_payload_volume(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadVolume(logtime, "PlayCommandIssued")

    def test_state__PlayCommandIssueda_VolumeState_payload_muted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadMuted(logtime, "PlayCommandIssued")



#PlayCommandIssued_SpeechState
    def test_state_PlayCommandIssued_SpeechState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechState(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_SpeechState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadToken(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_SpeechState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadOffsetInMilliseconds(logtime, "PlayCommandIssued")

    def test_state_PlayCommandIssued_SpeechState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadPlayerActivity(logtime, "PlayCommandIssued")


#PauseCommandIssued_PlaybackState
    def test_state_PauseCommandIssued_PlaybackState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackState(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_PlaybackState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadToken(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_PlaybackState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadOffsetInMilliseconds(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_PlaybackState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadPlayerActivity(logtime, "PauseCommandIssued")


#PauseCommandIssued_ViewState
    def test_state_PauseCommandIssued_ViewState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewState(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_ViewState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewStatePayloadToken(logtime, "PauseCommandIssued")



#PauseCommandIssued_AlertsState
    def test_state_PauseCommandIssued_AlertsState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsState(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_AlertsState_payload_allAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsToken(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_AlertsState_payload_allAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsType(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_AlertsState_payload_allAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsScheduledTime(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_AlertsState_payload_activeAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsToken(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_AlertsState_payload_activeAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsType(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_AlertsState_payload_activeAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsScheduledTime(logtime, "PauseCommandIssued")



#PauseCommandIssued_VolumeState
    def test_state_PauseCommandIssued_VolumeState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeState(logtime, "PauseCommandIssued")

    def test_state__PauseCommandIssued_VolumeState_payload_volume(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadVolume(logtime, "PauseCommandIssued")

    def test_state__PauseCommandIssueda_VolumeState_payload_muted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadMuted(logtime, "PauseCommandIssued")



#PauseCommandIssued_SpeechState
    def test_state_PauseCommandIssued_SpeechState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechState(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_SpeechState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadToken(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_SpeechState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadOffsetInMilliseconds(logtime, "PauseCommandIssued")

    def test_state_PauseCommandIssued_SpeechState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadPlayerActivity(logtime, "PauseCommandIssued")


#NextCommandIssued_PlaybackState
    def test_state_NextCommandIssued_PlaybackState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackState(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_PlaybackState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadToken(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_PlaybackState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadOffsetInMilliseconds(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_PlaybackState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadPlayerActivity(logtime, "NextCommandIssued")


#NextCommandIssued_ViewState
    def test_state_NextCommandIssued_ViewState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewState(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_ViewState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewStatePayloadToken(logtime, "NextCommandIssued")



#NextCommandIssued_AlertsState
    def test_state_NextCommandIssued_AlertsState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsState(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_AlertsState_payload_allAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsToken(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_AlertsState_payload_allAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsType(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_AlertsState_payload_allAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsScheduledTime(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_AlertsState_payload_activeAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsToken(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_AlertsState_payload_activeAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsType(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_AlertsState_payload_activeAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsScheduledTime(logtime, "NextCommandIssued")



#NextCommandIssued_VolumeState
    def test_state_NextCommandIssued_VolumeState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeState(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_VolumeState_payload_volume(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadVolume(logtime, "NextCommandIssued")

    def test_state_NextCommandIssueda_VolumeState_payload_muted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadMuted(logtime, "NextCommandIssued")



#NextCommandIssued_SpeechState
    def test_state_NextCommandIssued_SpeechState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechState(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_SpeechState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadToken(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_SpeechState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadOffsetInMilliseconds(logtime, "NextCommandIssued")

    def test_state_NextCommandIssued_SpeechState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadPlayerActivity(logtime, "NextCommandIssued")


#PreviousCommandIssued_PlaybackState
    def test_state_PreviousCommandIssued_PlaybackState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackState(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_PlaybackState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadToken(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_PlaybackState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadOffsetInMilliseconds(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_PlaybackState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStatePlaybackStatePayloadPlayerActivity(logtime, "PreviousCommandIssued")


#PreviousCommandIssued_ViewState
    def test_state_PreviousCommandIssued_ViewState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewState(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_ViewState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateViewStatePayloadToken(logtime, "PreviousCommandIssued")



#PreviousCommandIssued_AlertsState
    def test_state_PreviousCommandIssued_AlertsState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsState(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_AlertsState_payload_allAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsToken(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_AlertsState_payload_allAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsType(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_AlertsState_payload_allAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadAllAlertsScheduledTime(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_AlertsState_payload_activeAlerts_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsToken(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_AlertsState_payload_activeAlerts_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsType(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_AlertsState_payload_activeAlerts_scheduledTime(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateAlertsStatePayloadActiveAlertsScheduledTime(logtime, "PreviousCommandIssued")



#PreviousCommandIssued_VolumeState
    def test_state_PreviousCommandIssued_VolumeState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeState(logtime, "PreviousCommandIssued")

    def test_state__PreviousCommandIssued_VolumeState_payload_volume(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadVolume(logtime, "PreviousCommandIssued")

    def test_state__PreviousCommandIssueda_VolumeState_payload_muted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateVolumeStatePayloadMuted(logtime, "PreviousCommandIssued")



#PreviousCommandIssued_SpeechState
    def test_state_PreviousCommandIssued_SpeechState(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechState(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_SpeechState_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadToken(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_SpeechState_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadOffsetInMilliseconds(logtime, "PreviousCommandIssued")

    def test_state_PreviousCommandIssued_SpeechState_payload_playerActivity(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStateSpeechStatePayloadPlayerActivity(logtime, "PreviousCommandIssued")





#上海天气怎么样--ok
#多轮对话，比如query为“西藏天气”，云端在收到ListenStarted事件后，下发Listen指令。
#然后设备端开始播报云端发的交互信息，播报前发SpeechStarted事件。
#播报完成后，发SpeechFinished事件

#上海天气怎么样  的前一条
#设备端与服务端建立连接之后上报SynchronizeState事件，将设备端当前的状态与服务端进行同步
    def test_event_SynchronizeState(self):#
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSynchronizeState(logtime)

    def test_event_ListenStarted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventListenStarted(logtime)

    def test_event_ListenStarted_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventListenStartedPayloadHeaderMessageId(logtime)

    def test_event_ListenStarted_Header_DialogRequestId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventListenStartedPayloadHeaderDialogRequestId(logtime)

    def test_event_ListenStarted_PayloadFormat(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventListenStartedPayloadFormat(logtime)



#StopListen
    def test_directive_StopListen(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveStopListen(logtime)

    def test_directive_StopListen_header_messageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveStopListenHeaderMessageId(logtime)

    def test_directive_StopListen_header_dialogRequestId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveStopListenHeaderDialogRequestId(logtime)


#Speak
    def test_directive_Speak(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSpeak(logtime)

    def test_directive_Speak_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSpeakHeaderMessageId(logtime)

    def test_directive_Speak_Header_DialogRequestId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSpeakHeaderDialogRequestId(logtime)

    def test_directive_Speak_Payload_Format(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSpeakPayloadFormat(logtime)

    def test_directive_Speak_Payload_Token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSpeakPayloadToken(logtime)

    def test_directive_Speak_Payload_Url(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSpeakPayloadUrl(logtime)


#设备收到Speak指令后，在开始播报之前上报SpeechStarted事件
    def test_event_SpeechStarted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSpeechStarted(logtime)

    def test_event_SpeechStarted_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSpeechStartedHeaderMessageId(logtime)

    def test_event_SpeechStarted_Payload_Token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSpeechStartedPayloadToken(logtime)




#设备收到Speak指令后，播报完成，上报SpeechFinished事件
    def test_event_SpeechFinished(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSpeechFinished(logtime)

    def test_event_SpeechFinished_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSpeechFinishedHeaderMessageId(logtime)

    def test_event_SpeechFinished_Payload_Token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSpeechFinishedPayloadToken(logtime)





#播放刘德华的歌曲--ok
#在设备收到Play指令后，开始playback之前，需上报PlaybackStarted事件
#PlaybackStarted
    def test_event_PlaybackStarted(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStarted(logtime)

    def test_event_PlaybackStarted_Header_MessageId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStartedHeaderMessageId(logtime)

    def test_event_PlaybackStarted_payload_token(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStartedPayloadToken(logtime)

    def test_event_PlaybackStarted_payload_offsetInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStartedPayloadOffsetInMilliseconds(logtime)



#ProgressReportDelayElapsed
    def test_event_ProgressReportDelayElapsed(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportDelayElapsed(logtime)

    def test_event_ProgressReportDelayElapsed_Header_MessageId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportDelayElapsedHeaderMessageId(logtime)

    def test_event_ProgressReportDelayElapsed_payload_token(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportDelayElapsedPayloadToken(logtime)

    def test_evten_ProgressReportDelayElapsed_payload_offsetInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportDelayElapsedPayloadOffsetInMilliseconds(logtime)



#ProgressReportIntervalElapsed
    def test_event_ProgressReportIntervalElapsed(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportIntervalElapsed(logtime)

    def test_event_ProgressReportIntervalElapsed_Header_MessageId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportIntervalElapsedHeaderMessageId(logtime)

    def test_event_ProgressReportDelayElapsed_payload_token(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportIntervalElapsedPayloadToken(logtime)

    def test_event_ProgressReportIntervalElapsed_payload_offsetInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventProgressReportIntervalElapsedPayloadOffsetInMilliseconds(logtime)




#播报audio item过程中，收到Stop指令，设备端在执行完stop后，上报PlaybackStoped事件
    def test_event_PlaybackStopped(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStopped(logtime)

    def test_event_PlaybackStopped_Header_MessageId(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStoppedHeaderMessageId(logtime)

    def test_event_PlaybackStopped_payload_token(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStoppedPayloadToken(logtime)

    def test_event_PlaybackStopped_payload_offsetInMilliseconds(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStoppeddPayloadOffsetInMilliseconds(logtime)



#在audio item播放快要结束时候，上报PlaybackNearlyFinished事件
    def test_event_PlaybackNearlyFinished(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackNearlyFinished(logtime)

    def test_event_PlaybackNearlyFinished_Header_MessageId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackNearlyFinishedHeaderMessageId(logtime)

    def test_event_PlaybackNearlyFinished_payload_token(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackNearlyFinishedPayloadToken(logtime)

    def test_event_PlaybackNearlyFinished_payload_offsetInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackNearlyFinishedPayloadOffsetInMilliseconds(logtime)



#Play
    def test_directive_Play(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectivePlay(logtime)

    def test_directive_Play_Header_MessageId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayHeaderMessageId(logtime)

    def test_directive_Play_Header_dialogRequestId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayHeaderDialogRequestId(logtime)

    def test_directive_Play_Payload_playBehavior_ENQUEUE_expectedPreviousToken(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadPlayBehaviorENQUEUEExpectedPreviousToken(logtime)

    def test_directive_Play_Payload_playBehavior_REPLACE_ENQUEUED_expectedPreviousToken(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadPlayBehaviorREPLACEENQUEUEDExpectedPreviousToken(logtime)

    def test_directive_Play_Payload_playBehavior_REPLACEALL(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadPlayBehaviorREPLACEALL(logtime)

    def test_directive_Play_Payload_AudioItem_audioItemId(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemAudioItemId(logtime)

    def test_directive_Play_Payload_AudioItem_stream_url(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemStream_url(logtime)

    def test_directive_Play_Payload_AudioItem_Stream_StreamFormat(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemStreamStreamFormat(logtime)

    def test_directive_Play_Payload_AudioItem_stream_offsetInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemStreamOffsetInMilliseconds(logtime)

    def test_directive_Play_Payload_AudioItem_Stream_ExpiryTime(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemStreamExpiryTime(logtime)

    def test_directive_Play_Payload_AudioItem_stream_progressReport_progressReportDelayInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemStreamProgressReportProgressReportDelayInMilliseconds(logtime)

    def test_directive_Play_Payload_AudioItem_stream_progressReport_progressReportIntervalInMilliseconds(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayPayloadAudioItemStreamProgressReportProgressReportIntervalInMilliseconds(logtime)

    def test_directive_Play_AudioItem_stream_token(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectivePlayAudioItemStreamToken(logtime)




#在audio item播放结束时，上报PlaybackFinished事件
    def test_event_PlaybackFinished(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackFinished(logtime)

    def test_event_PlaybackFinished_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackFinishedHeaderMessageId(logtime)

    def test_event_PlaybackFinished_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackFinishedPayloadToken(logtime)

    def test_event_PlaybackFinished_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackFinishedPayloadOffsetInMilliseconds(logtime)


#当用户按了设备端上的暂停按钮时（音乐播放过程中），上报PauseCommandIssued事件--need check
    def test_event_PauseCommandIssued(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPauseCommandIssued(logtime)

#当用户按了设备端上的播放按钮时（音乐播放已暂停），上报PlayCommandIssued事件--need check
    def test_event_PlayCommandIssued(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlayCommandIssued(logtime)

#当用户按了设备端上的下一首按钮时（音乐播放过程中），上报NextCommandIssued事件--need check
    def test_event_NextCommandIssued(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventNextCommandIssued(logtime)

#当用户按了设备端上的上一首按钮时（音乐播放过程中），上报PreviousCommandIssued事件--need check
    def test_event_PreviousCommandIssued(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPreviousCommandIssued(logtime)



#音量设置为三十--ok

#在收到SetVolume或者AdjuestVolume指令后，音量操作完成，上报VolumeChanged事件
    def test_directive_setVolume(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetVolume(logtime)

    def test_directive_setVolume_Header_MessageId(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetVolumeHeaderMessageId(logtime)

    def test_directive_setVolume_Header_dialogRequestId(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetVolumeHeaderDialogRequestId(logtime)

    def test_directive_setVolume_Payload_volume(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetVolumePayloadVolume(logtime)



#VolumeChanged
    def test_event_VolumeChanged(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventVolumeChanged(logtime)

    def test_event_VolumeChanged_Header_MessageId(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventVolumeChangedHeaderMessageId(logtime)

    def test_event_VolumeChanged_Payload_Volume(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventVolumeChangedPayloadVolume(logtime)

    def test_event_VolumeChangedPayloadMuted(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventVolumeChangedPayloadMuted(logtime)



#音量减小二十
#AdjustVolume
    def test_Directive_AdjustVolume(self):
        query = querydict['10']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveAdjustVolume(logtime)

    def test_event_AdjustVolume_Header_MessageId(self):
        query = querydict['10']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveAdjustVolumeHeaderMessageId(logtime)

    def test_event_AdjustVolume_Header_dialogRequestId(self):
        query = querydict['10']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveAdjustVolumeHeaderDialogRequestId(logtime)

    def test_event_AdjustVolume_Payload_volume(self):
        query = querydict['10']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveAdjustVolumePayloadVolume(logtime)



#静音--ok
    def test_event_SetMute(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetMute(logtime)

    def test_event_SetMute_Header_MessageId(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetMuteHeaderMessageId(logtime)

    def test_event_SetMute_Header_dialogRequestId(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetMuteHeaderDialogRequestId(logtime)

    def test_event_SetMute_Payload_mute(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveSetMutePayloadMute(logtime)




#在设备端收到SetMute指令后，操作完成，上报muteChanged事件
    def test_event_MuteChanged(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventMuteChanged(logtime)


    def test_event_MuteChanged_Header_MessageId(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventMuteChangedHeaderMessageId(logtime)


    def test_event_MuteChanged_Payload_Volume(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventMuteChangedPayloadVolume(logtime)


    def test_event_MuteChanged_Payload_Muted(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventMuteChangedPayloadMuted(logtime)




#播放林俊杰的歌曲-今天天气怎么样--ok
    def test_event_PlaybackPaused(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackPaused(logtime)

    def test_event_PlaybackPaused_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackPausedHeaderMessageId(logtime)

    def test_event_PlaybackPaused_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackPausedPayloadToken(logtime)

    def test_event_PlaybackPaused_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackPausedPayloadOffsetInMilliseconds(logtime)



#暂停--ok
    def test_directive_Stop(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveStop(logtime)

    def test_directive_Stop_Header_MessageId(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveStopHeaderMessageId(logtime)

    def test_directive_Stop_Header_dialogRequestId(self):
        query = querydict['12']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkDirectiveStopHeaderDialogRequestId(logtime)



#创建一个闹钟--ok
    def test_directive_Listen(self):
        query = querydict['14']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveListen(logtime)

    def test_directive_Listen_Header_MessageId(self):
        query = querydict['14']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveListenHeaderMessageId(logtime)

    def test_directive_Listen_Header_DialogRequestId(self):
        query = querydict['14']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveListenHeaderDialogRequestId(logtime)

    def test_directive_Listen_Payload_TimeoutInMilliseconds(self):
        query = querydict['14']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveListenPayloadTimeoutInMilliseconds(logtime)



#一分钟之后提醒我开会（等着闹钟响起，注意后台无音乐播放）--ok
#设备端收到SetAlert指令，闹钟设置成功之后，上报该事件给服务端。
    def test_directive_SetAlert(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSetAlert(logtime)

    def test_directive_SetAlert_Header_MessageId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSetAlertHeaderMessageId(logtime)

    def test_directive_SetAlert_Header_DialogRequestId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSetAlertHeaderDialogRequestId(logtime)

    def test_directive_SetAlert_Payload_Token(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSetAlertPayloadToken(logtime)

    def test_directive_SetAlert_Payload_Type(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSetAlertPayloadType(logtime)

    def test_directive_SetAlert_Payload_ScheduledTime(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveSetAlertPayloadScheduledTime(logtime)



#SetAlertSucceeded
    def test_event_SetAlertSucceeded(self):#
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSetAlertSucceeded(logtime)

    def test_event_SetAlertSucceeded_Header_MessageId(self):#
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSetAlertSucceededHeaderMessageId(logtime)

    def test_event_SetAlertSucceeded_Payload_Token(self):#
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventSetAlertSucceededPayloadToken(logtime)




#到了定点时间，触发了闹钟，闹铃开始响起时上报AlertStarted事件
    def test_event_AlertStarted(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertStarted(logtime)

    def test_event_AlertStarted_Header_MessageId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertStartedHeaderMessageId(logtime)

    def test_event_AlertStarted_Payload_Token(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertStartedPayloadToken(logtime)




#闹铃响起时Alert Channel在前景（意味着Dialog Channel在非活跃状态），或者在闹铃播放当中Dialog Channel从活跃状态进入非活跃状态时（意味着Alert Channel从背景变为前景），上报AlertEnteredForeground事件
    def test_event_AlertEnteredForeground(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredForeground(logtime)

    def test_event_AlertEnteredForeground_Header_MessageId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredForegroundHeaderMessageId(logtime)

    def test_event_AlertEnteredForeground_Payload_Token(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredForegroundPayloadToken(logtime)

#
#设备端停止正在播放的闹钟，应上报AlertStopped事件设备端停止正在播放的闹钟，应上报AlertStopped事件
    def test_event_AlertStopped(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertStopped(logtime)

    def test_event_AlertStopped_Header_MessageId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertStoppedHeaderMessageId(logtime)

    def test_event_AlertStopped_Payload_Token(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertStoppedPayloadToken(logtime)

#AlertEnteredForeground
    def test_event_AlertEnteredForeground(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredForeground(logtime)

    def test_event_AlertEnteredForeground_Header_MessageId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredForegroundHeaderMessageId(logtime)

    def test_event_AlertEnteredForeground_Payload_Token(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredForegroundPayloadToken(logtime)



#一分钟之后提醒我开会-成都天气怎么样--ok
    def test_event_PlaybackResumed(self):
        query = querydict['17']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackResumed(logtime)

    def test_event_PlaybackResumed_Header_MessageId(self):
        query = querydict['17']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackResumedHeaderMessageId(logtime)

    def test_event_PlaybackResumed_payload_token(self):
        query = querydict['17']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackResumedPayloadToken(logtime)

    def test_event_PlaybackResumed_payload_offsetInMilliseconds(self):
        query = querydict['17']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackResumedPayloadOffsetInMilliseconds(logtime)



#一分钟后提醒我开会-闹钟响起后-今天天气怎么样
#闹铃播放当中，用户开始了语音请求，或者服务端下发了Speak指令，Dialog Channel从非活跃状态进入了活跃状态（意味着Alert Channel从前景变味背景），上报AlertEnteredBackground事件
    def test_event_AlertEnteredBackground(self):
        query = querydict['17']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredBackground(logtime)

    def test_event_AlertEnteredBackground_Header_MessageId(self):
        query = querydict['15']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredBackgroundHeaderMessageId(logtime)

    def test_event_AlertEnteredBackground_Payload_Token(self):
        query = querydict['17']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventAlertEnteredBackgroundPayloadToken(logtime)



#删除闹钟
    def test_event_DeleteAlertSucceeded(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#       print 'test_logtime:',logtime
        self.checkEventDeleteAlertSucceeded(logtime)

    def test_event_DeleteAlertSucceeded_HeaderMessageId(self):#
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventDeleteAlertSucceededHeaderMessageId(logtime)

    def test_event_DeleteAlertSucceeded_PayloadToken(self):#
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventDeleteAlertSucceededPayloadToken(logtime)




#设备端收到DeleteAlert指令后，删除对应的闹钟
    def test_directive_DeleteAlert(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#       print 'test_logtime:',logtime
        self.checkDirectiveDeleteAlert(logtime)

    def test_directive_DeleteAlert_Header_MessageId(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveDeleteAlertHeaderMessageId(logtime)

    def test_directive_DeleteAlert_Header_DialogRequestId(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveDeleteAlertHeaderDialogRequestId(logtime)


    def test_directive_DeleteAlert_Payload_Token(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDirectiveDeleteAlertPayloadToken(logtime)


#网速较慢时PlaybackStutterStarted
    def test_event_PlaybackStutterStarted(self):
        query = querydict['16']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterStarted(logtime)

    def test_event_PlaybackStutterStarted_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterStartedHeaderMessageId(logtime)

    def test_event_PlaybackStutterStarted_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterStartedPayloadToken(logtime)

    def test_event_PlaybackStutterStarted_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterStartedPayloadOffsetInMilliseconds(logtime)

#网速较慢时PlaybackStutterFinished
    def test_event_PlaybackStutterFinished(self):
        query = querydict['16']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterFinished(logtime)

    def test_event_PlaybackStutterFinished_Header_MessageId(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterFinishedHeaderMessageId(logtime)

    def test_event_PlaybackStutterFinished_payload_token(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterFinishedPayloadToken(logtime)

    def test_event_PlaybackStutterFinished_payload_offsetInMilliseconds(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventPlaybackStutterFinishedPayloadOffsetInMilliseconds(logtime)


#屏幕展示
    def test_directive_HtmlView(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#       print 'test_logtime:',logtime
        self.checkDirectiveHtmlView(logtime)

    def test_directive_HtmlView_header_messageId(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#       print 'test_logtime:',logtime
        self.checkDirectiveHtmlViewHeaderMessageId(logtime)

    def test_directive_HtmlView_payload_url(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#       print 'test_logtime:',logtime
        self.checkDirectiveHtmlViewPayloadUrl(logtime)

    def test_directive_HtmlView_payload_token(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#       print 'test_logtime:',logtime
        self.checkDirectiveHtmlViewPayloadToken(logtime)


#设备端每隔一个小时需要上报UserInactivityReport事件，报告自最近一次用户交互以来所经过的时间
    def test_event_UserInactivityReport(self):
        query = querydict['16']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventUserInactivityReport(logtime)

    def test_event_UserInactivityReport_Payload_InactiveTimeInSeconds(self):
        query = querydict['16']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkEventUserInactivityReportPayloadInactiveTimeInSeconds(logtime)



#设备在收到指令，但不识别，无法执行的时候，上报ExceptionEncountered事件
    def test_event_ExceptionEncountered(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventExceptionEncountered(logtime)#播放赵雷的成都

    def test_event_ExceptionEncountered_Payload_unparsedDirective(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventExceptionEncountered(logtime)

    def test_event_ExceptionEncountered_Payload_error_type(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventExceptionEncountered(logtime)

    def test_event_ExceptionEncountered_Payload_error_message(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
        self.checkEventExceptionEncountered(logtime)





#检查上报一个事件后是否下发指令
    def test_ListenStarted_StopListen(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkListenStartedAndStopListen(logtime)

    def test_ListenStarted_Speak(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkListenStartedAndSpeak(logtime)

    def test_Speak_SpeechStarted(self):
        query = querydict['1']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkSpeakAndSpeechStarted(logtime)


    def test_SetVolume_VolumeChanged(self):
        query = querydict['9']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkSetVolumeAndVolumeChanged(logtime)

    def test_AjustVolume_VolumeChanged(self):
        query = querydict['10']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkAdjustVolumeAndVolumeChanged(logtime)


    def test_SetMute_MutedChanged(self):
        query = querydict['13']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkSetMuteAndMutedChanged(logtime)

#如果Play指令中有progressReportDelayInMilliseconds，则对应audio item播放此时间长后需要上报ProgressReportDelayElapsed事件
    def test_Play_progressReportDelayInMilliseconds_ProgressReportDelayElapsed(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkPlayProgressReportDelayInMillisecondsProgressReportDelayElapsed(logtime)


#如果Play指令有progressReportIntervalInMilliseconds，则在播放对应audio item时，每隔此时间上报ProgressReportIntervalElapsed事件。
    def test_Play_progressReportIntervalInMilliseconds_ProgressReportIntervalElapsed(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkPlayProgressReportIntervalInMillisecondsProgressReportIntervalElapsed(logtime)

    #在PlaybackStarted事件之后，如果设备端缓冲音频数据慢于播放速度时，上报PlaybackStutterStarted事件
    def test_PlaybackStarted_PlaybackStutterStarted(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkPlaybackStartedPlaybackStutterStarted(logtime)

    #PlaybackStutterStarted事件之后，缓冲恢复到正常状态，可重新开始播放时上报PlaybackStutterFinished事件
    def test_PlaybackStutterStarted_PlaybackStutterFinished(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkPlaybackStutterStartedPlaybackStutterFinished(logtime)

    #收到Stop指令，停止了播放上报PlaybackStopped事件
    def test_Stop_PlaybackStopped(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkStopPlaybackStopped(logtime)

    #收到了Play指令，playBehavior为REPLACE_ALL，停止了当前音频流的播上报PlaybackStopped事件
    def test_Play_playBehavior_REPLACE_ALL_PlaybackStopped(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkPlayBehaviorREPLACE_ALLPlaybackStopped(logtime)

    #设备端处理完ClearQueue指令后上报PlaybackQueueCleared
    def test_checkClearQueue_PlaybackQueueCleared(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkClearQueuePlaybackQueueCleared(logtime)

    #设备端处理完ClearQueue指令后上报PlaybackQueueCleared
    def test_SetAlert_SetAlertSucceeded(self):
        query = querydict['2']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkSetAlertSetAlertSucceeded(logtime)

    #设备端处理完ClearQueue指令后上报PlaybackQueueCleared
    def test_DeleteAlert_DeleteAlertSucceeded(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDeleteAlertDeleteAlertSucceeded(logtime)

    #收到DeleteAlert指令，停止了正在闹铃中的闹钟，上报AlertStopped
    def test_DeleteAlert_AlertStopped(self):
        query = querydict['19']
        print query.decode('utf-8')
        logtime = self.getLogtimeToQuery(query)
#        print 'test_logtime:',logtime
        self.checkDeleteAlertAlertStopped(logtime)


'''

#SetEndpoint
#ThrowException



