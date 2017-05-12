# -*- coding:utf-8 -*-
import os
import time
import datetime
import logging
import logging.handlers

# 创建一个logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

_logPath = os.path.abspath("log")
_prepend = "log-"
_suffix = ".log"
_logFileName = os.path.join(
    _logPath, "{}{}{}".format(_prepend, time.strftime("%Y%m%d"), _suffix))

# 创建一个handler，用于写入日志文件
# fh = logging.FileHandler(_logFileName, "a", "utf-8")
# fh.setLevel(logging.DEBUG)

# timed rotating
fh = logging.handlers.TimedRotatingFileHandler(filename=_logFileName,
                                               when="midnight",
                                               interval=1,
                                               backupCount=60,
                                               encoding="utf-8")
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter(
    '%(asctime)s %(levelname).1s %(name)s %(filename)s(%(lineno)d): %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)


# 给 logger 添加handler
logger.addHandler(fh)
logger.addHandler(ch)


# 缓存
# class MyHandler(logging.handlers.MemoryHandler):

#     lastRecordDate = None

#     def shouldFlush(self, record):
#         # 在日期变化时, 强制 Flush, 保证每天生成日志文件
#         recordDate = datetime.date.fromtimestamp(record.created)
#         if self.lastRecordDate != recordDate:
#             self.lastRecordDate = recordDate
#             return True
#         return super(MyHandler, self).shouldFlush(record)


# _memoryHandler = MyHandler(1,
#                            flushLevel=logging._checkLevel("ERROR"),
#                            target=fh)

# logging.getLogger().addHandler(_memoryHandler)
