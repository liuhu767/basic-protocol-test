# basic-protocol-test
基础协议的字段校验

第一步：根据设备的功能选择querylist.txt里的query进行测试

第二步：填写设备的cuid、测试的时间、保存日志的文件名称，运行lib下的GetLogFile.py

第三步：根据设备的功能在TestDcsCase.py修改测试用例

第四步：执行测试命令 nosetests -s -v TestDcsCase.py

