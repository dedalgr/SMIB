#-*- coding:utf-8 -*-
'''
Created on 12.09.2018 г.

@author: dedal
'''
import logging
from logging.handlers import SysLogHandler, RotatingFileHandler, SocketHandler, DatagramHandler
            
class StreamToLogger(object):
    """
       Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

class MySysLogHandler(SysLogHandler):
    def __init__(self, ident):
        self.ident = ident
        SysLogHandler.__init__(self, address='/dev/log')

    def emit(self, record):
        priority = self.encodePriority(self.facility, self.mapPriority(record.levelname))
        record.ident = self.ident
        super(MySysLogHandler, self).emit(record)

class MySocketLogHandler(SocketHandler):
    def __init__(self, adress, port, ident='' ):
        self.ident = ident
        SocketHandler.__init__(self, adress, port)

    def emit(self, record):
        # priority = self.encodePriority(self.facility, self.mapPriority(record.levelname))
        record.ident = self.ident
        super(MySocketLogHandler, self).emit(record)
        self.close()


class MyRotatingFileHandler(RotatingFileHandler):

    def __init__(self, log_name, maxBytes, backupCount):
        RotatingFileHandler.__init__(self, log_name, mode='a',
                            maxBytes=maxBytes,
                            backupCount=backupCount,
                            encoding=None,
                            delay=0)

    # def emit(self, record):
    #     priority = self.encodePriority(self.facility, self.mapPriority(record.levelname))
    #     super(MyRotatingFileHandler, self).emit(record)
if __name__ == '__main__':
    from multiprocessing import log_to_stderr
    socketh_handler = MySocketLogHandler(
        '127.0.0.1',
        9020,
        1
    )
    log_net_formatter = logging.Formatter('%(ident)s %(asctime)s:%(levelname)s:%(name)s:%(message)s')
    socketh_handler.setFormatter(log_net_formatter)
    socketh_handler.setLevel(logging.INFO)
    log = log_to_stderr(logging.INFO)
    log.addHandler(socketh_handler)
    log.error('test 1')
    log.error('test 2')
