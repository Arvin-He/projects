# -*- coding:utf-8 -*-
import os
import time
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
# timed rotating
fh = logging.handlers.TimedRotatingFileHandler(filename=_logFileName,
                                               when="midnight",
                                               interval=1,
                                               backupCount=60,
                                               encoding="utf-8")
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter(
    '%(asctime)s %(levelname).1s %(name)s %(filename)s(%(lineno)d): %(message)s')
fh.setFormatter(formatter)


# 给 logger 添加handler
logger.addHandler(fh)
