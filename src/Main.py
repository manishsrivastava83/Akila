import tornado.ioloop
from tornado.ioloop import IOLoop
import tornado.web
from tornado.web import URLSpec as url
from TwilioRequestHandler import TwilioRequestHandler
from AccountsEndPoint import AccountsEndPoint
from tornado.options import define, options, parse_command_line

define("port", default=3000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

#class TwilioRequestHandler(tornado.web.RequestHandler):
#    def get(self,url):
#        self.write("Hi Sandeep, Welcome to Tornado Web Framework.")

#Portal handler
#Twilio handler
#FB Handler

def make_app():
    return tornado.web.Application([
        #(r"/abc/v1/message", TwilioRequestHandler),
        #(r"/api/v1/twilio/sms", TwilioRequestHandler),
        (r"/welcome/sms/reply", TwilioRequestHandler),
        (r"/portal/v1/accounts", AccountsEndPoint)
    ],
    debug=options.debug,)

#Check following for 
#http://www.tornadoweb.org/en/stable/guide/running.html
#Due to the Python GIL (Global Interpreter Lock), it is necessary to run multiple Python processes to take full advantage of multi-CPU machines. Typically it is best to run one process per CPU.
def main():
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    #server = tornado.httpserver.HTTPServer(app)
    #server.listen(8080)
    #server.bind(3000)
    #server.start(0)  # forks one process per cpu
    #IOLoop.current().start()

if __name__ == "__main__":
    main()
#
#    application = tornado.web.Application([
#        (r"/mStoreRoot/V1/FCS/(.*)", TwilioRequestHandler),
#    ])
#    application.listen(8888)
#    tornado.ioloop.IOLoop.instance().start()
