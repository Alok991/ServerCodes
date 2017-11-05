from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
import sys

class MyClientProtocol(WebSocketClientProtocol):
    
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
    
    def onOpen(self):
    
      str=raw_input("\n")
      self.sendMessage(str.encode('utf8'))
        
     
    def onMessage(self, payload, isBinary):

        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        print payload
        list=payload.mongodecode('utf8').split("-")
       
        sd=raw_input("\n")
        self.sendMessage(sd.encode('utf8'))  

  

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000",)
    factory.protocol = MyClientProtocol
    factory.setProtocolOptions(autoPingInterval=100,autoPingTimeout=050)

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()