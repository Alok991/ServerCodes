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
                str1=raw_input("For new registration R      , For loggingIn L \n")
            #print "after Raw_input"
                if str1 == "R" or str1== "r":
                    self.name= raw_input("Enter your name:  \n")
                    self.phNo =raw_input("Enter your Phone number:\n")
                    self.email=raw_input("Enter your email id:\n")
                    self.pass1=raw_input("Enter your password:\n")
                    self.dob=raw_input("Enter your date of birth in ddmmyyyy\n")
                    self.sex=raw_input("Enter your sex in M/F/O\n")
                    self.aadhaar=raw_input("Enter your aadhaar \n")
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
                    self.sendMessage(s.encode('utf8'))
                elif str1 =="L" or str1== "l":
                    self.phNo=raw_input("Enter your PhoneNumber :\n")
                    self.pass1= raw_input("Enter your password : \n")
                    s="A-L-"+self.phNo+"---"+self.pass1
                    self.sendMessage(s.encode('utf8'))



        
        #   str4=raw_input("do you want to change the state of devices Y/N \n")
         #       if str4=="Y" or str4=="y":
          #        sa="A-LC-"+list[0]+"---"+list[1]
           #       self.sendMessage(sa.encode('utf8'))
            #      self.str3=raw_input("enter device state\n")
             #     list1=self.str3.decode('utf8').split("-")
              #    s1="A-E-"+list[0]+"-"+list1[0]+"-"+list1[1]+"-"+list1[2]
               #   self.sendMessage(s1.encode('utf8'))
                #  self.str41=raw_input("Client Enters new device states :\n")
                 # list2=self.str41.decode('utf8').split("-")
                  #s411="E-"+list[0]+"-"+list2[0]+"-"+list2[1]+"-"+list2[2]
                  #self.sendMessage(s411.encode('utf8'))                      

 

          #if s==NULL
          #else hello() 
          # self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
  #          self.factory.reactor.callLater(1, hello)

        # start sending messages every second ..
 #       hello() 

    #def onMessage(self, payload, isBinary):
     #   if isBinary:
      #      print("Binary message received: {0} bytes".format(len(payload)))
       # else:
        #    print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000",)
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()