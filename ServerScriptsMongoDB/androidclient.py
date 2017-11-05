from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
import sys

class MyClientProtocol(WebSocketClientProtocol):
    str2=""
    str3=""
    cookie= None
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
    def onMessage(self, payload, isBinary):

        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        part =   payload.decode('utf8').split("-")

        if part[0]=="S" and part[1]== "R" and part[2]=="C":
            self.cookie=part[3]
        if part[0]=="S" and part[1]=="L" and part[2]=="C":
            self.cookie=part[3]
                   

        #if part[0]=="S" and part[1]=="CE":





            
    
    def onOpen(self):
        
        print("WebSocket connection open.")

        if self.cookie != None:
         self.sendMessage("A"+"-"+"LC"-cookie.encode('utf8'))


        else:

            #def hello():
            #self.sendMessage(u"A-R-Vaishalshah-1234567890-1234-Pass#2word".encode('utf8'))
          
            #print "hello func"
                str1=raw_input("For new registration R      , For loggingIn L,For cookie in C \n")
            #print "after Raw_input"
                if str1 == "R" or str1== "r":
                    self.name= raw_input("Enter your name:  \n")
                    self.phNo =raw_input("Enter your Phone number:\n")
                    self.email=raw_input("Enter your email id:\n")
                    self.pass1=raw_input("Enter your password:\n")
                    self.dob=raw_input("Enter your date of birth in ddmmyyyy\n")
                    self.sex=raw_input("Enter your sex in M/F/O\n")
                    self.aadhaar=raw_input("Enter your aadhaar \n")
                    '''
                    self.initial_address=raw_input("Enter your addrees \n")
                    self.location_longitude=raw_input("Enter longitude\n")
                    self.location_latitude=raw_input("Enter latitude\n")
                    self.home_permanent=1
                    self.home_permanentid=""
                    self.count_perm=0
                    while self.home_permanent==1:
                          accept=raw_input("do you want to enter home_permanentid\n")
                          if accept=="y" or accept=="Y":
                             tem=raw_input("Enter home_permanentid\n")
                             #self.home_permanentid=tem
                             self.home_permanentid=self.home_permanentid+tem+"-"
                             self.home_permanent=1
                             self.count_perm+=1
                          else :
                              self.home_permanent=0

                    self.home_temp=1
                    self.home_tempid=""
                    self.count_temp=0
                    while self.home_temp==1:
                          accept=raw_input("do you want to enter home_tempid\n")
                          if accept=="y" or accept=="Y":
                             tem=raw_input("Enter home_tempid\n")
                             #self.home_tempid+=tem
                             self.home_tempid=self.home_tempid+tem+"-"
                             self.home_temp=1
                             self.count_temp+=1
                          else :
                              self.home_temp=0

                    #self.home_permanentid=raw_input("Enter home_permanentid :\n")
                    


#-Enter your phone number : -Enter your  id  : -Enter your password :\n")
                    s="A-R-"+self.name+"-"+self.phNo+"-"+self.email+"-"+self.pass1+"-"+self.sex+"-"+self.dob+"-"+self.aadhaar+"-"+self.initial_address+"-"+self.location_longitude+"-"+self.location_latitude+"-"+str(self.count_perm)+"-"+self.home_permanentid+str(self.count_temp)+"-"+self.home_tempid
                    s=s[:-1]
                    '''
                    s="A-A-"+self.name+"-"+self.phNo+"-"+self.pass1+"-"+self.email+"-"+self.sex+"-"+self.dob+"-"+self.aadhaar
                    self.sendMessage(s.encode('utf8'))
                elif str1 =="L" or str1== "l":
                    self.phNo=raw_input("Enter your PhoneNumber :\n")
                    self.pass1= raw_input("Enter your password : \n")
                    s="A-B-"+self.phNo+"-"+self.pass1
                    self.sendMessage(s.encode('utf8'))
                elif str1 =="c" or str1=="C":
                  c=raw_input("enter the cookie:\n")
                  s="A-C-"+c
                  self.sendMessage(s.encode('utf8'))
                else:
                  st=raw_input("\n")
                  print st 
                  self.sendMessage(st.encode('utf8'))



    
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