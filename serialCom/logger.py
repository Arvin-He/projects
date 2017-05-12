# -*- coding:utf-8 -*-

import logging

# 创建一个logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler("my_log.log", "a", "utf-8")
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s- [%(filename)s:%(lineno)s]')
fh.setFormatter(formatter)
ch.setFormatter(formatter)


# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# import os
# import datetime
# import logging
# import logging.handlers

# # _config = basic.baseSysData("ini/basic.log.ini")


# # 配置日志等级
# for name, level in _config["Level"].items():
#     logging.getLogger(name).setLevel(level)


# # 将日志保存到文件
# _logFileName = basic.absLogPath(_config["Handler"]["fileName"])
# os.makedirs(os.path.dirname(_logFileName), exist_ok=True)

# # timed rotating
# _fileHandler = logging.handlers.TimedRotatingFileHandler(
#     _logFileName,
#     when=_config["Handler"]["when"],
#     interval=int(_config["Handler"]["interval"]),
#     backupCount=int(_config["Handler"]["backupCount"]),
#     encoding="utf-8")

# # 格式化
# _formatter = logging.Formatter(
#     _config["Handler"]["format"],
#     _config["Handler"]["dateFormat"])
# _fileHandler.setFormatter(_formatter)


# # 缓存
# class MyHandler(logging.handlers.MemoryHandler):

#     lastRecordDate = None

#     def shouldFlush(self, record):
#         # 在日期变化时, 强制 Flush, 保证每天生成日志文件
#         recordDate = datetime.date.fromtimestamp(record.created)
#         if self.lastRecordDate != recordDate:
#             self.lastRecordDate = recordDate
#             return True
#         return super(MyHandler, self).shouldFlush(record)


# _memoryHandler = MyHandler(int(_config["Handler"]["capacity"]),
#                            flushLevel=logging._checkLevel(
#                                _config["Handler"]["flushLevel"]),
#                            target=_fileHandler)
