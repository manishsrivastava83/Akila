import zmq
import logging
import logging.config
import json
import time

logConfigFile = "config/LoggerConfig.json"

class LoggerClient:
     __shared_state = {}

     #TODO Dependency injection for config
     def __init__(self):
         self.__dict__ = self.__shared_state
         with open(logConfigFile, "r") as fd:
             self.LoggerConfig=json.load(fd)
             print(self.LoggerConfig['port'])
         self.context = zmq.Context()
         self.socket = self.context.socket(zmq.PUB)
         self.socket.bind("tcp://*:%s" % self.LoggerConfig['port'])

     def sendLogMessage(self,msg):
         #self.socket.send_string("%s %s" % (self.LoggerConfig['topic'], str(msg)))
         print(msg)

#logger = LoggerClient()
#while True:
#    msg = {'@message': 'python test-1 message', '@tags': ['python', 'test']}
#    print(msg)
#    logger.sendLogMessage(msg)
#    time.sleep(1)
