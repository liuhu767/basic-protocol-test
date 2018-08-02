# basic-protocol-test
基础协议的字段校验

8个设备的能力：语音输入、语音输出、扬声器控制、音频播放器、播放控制、闹钟、屏幕显示、系统
详细见：
https://dueros.baidu.com/didp/doc/dueros-conversational-service/device-interface/voice-input_markdown

检验上报的事件、设备的状态、服务端下发给设备的指令。

第一步：根据设备的功能选择querylist.txt里的query进行测试

第二步：填写设备的cuid、测试的时间、保存日志的文件名称，运行lib下的GetLogFile.py

第三步：根据设备的功能在TestDcsCase.py修改测试用例

第四步：执行测试命令 nosetests -s -v TestDcsCase.py

