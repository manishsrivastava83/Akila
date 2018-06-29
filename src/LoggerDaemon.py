import zmq
import logging
import logging.config
import json

logConfigFile = "config/LoggerConfig.json"

class Logger:
     __shared_state = {}

     def constructListeningAddress(self):
         #Assert for ZeroMq config
         #Regroup ZeroMQ config in 
         return self.LoggerConfig['protocol']+"://"+self.LoggerConfig['fqdn']+":"+str(self.LoggerConfig['port'])

     #TODO Dependency injection for config
     def __init__(self):
         self.__dict__ = self.__shared_state
         #self.configFd=open("LogConfing.json", "r")
         #TODO introduce a function
         logging.basicConfig()
         with open(logConfigFile, "r") as fd:
             self.LoggerConfig=json.load(fd)
             logging.config.dictConfig(self.LoggerConfig)
             print(self.LoggerConfig['port'])

         #TODO introduce a function
         self.context = zmq.Context()
         self.socket = self.context.socket(zmq.SUB)
         self.socket.setsockopt_string(zmq.SUBSCRIBE, self.LoggerConfig['topic'])
         print(self.LoggerConfig['topic'])
         self.socket.connect(self.constructListeningAddress())

         #TODO introduce a function for logging context
         logging.config.dictConfig(self.LoggerConfig)
         self.logger = logging.getLogger()  # Returns the "root" logger
         #print(logger.getEffectiveLevel())  # Check what level of messages will be shown
         #logger.debug("Test debug message")
         #logger.info("Test info message")
         #logger.warn("Test warning message")
         #logger.error("Test error message")
         #logger.critical("Test critical message")

     def start(self):
         while True:    
             string = self.socket.recv()
             print(string)
             self.logger.debug(string)

def main():
    loggerDaemon = Logger()
    loggerDaemon.start()

if __name__ == '__main__':
    main()
