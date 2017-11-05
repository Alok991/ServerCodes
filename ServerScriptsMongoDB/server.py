from pymongo import MongoClient
import sys
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import Cookie
import gc
import hashlib
import time
import demjson

from pymongo import IndexModel, ASCENDING, DESCENDING




client = MongoClient('localhost', 27017)
db = client.alive
alive_user = db.user
alive_history=db.history
alive_home=db.home
alive_product=db.product
#Clients = {None:None}
#index1 = IndexModel([("_id", DESCENDING)])
db.user.create_index([("_id",-1)],background=True)
db.home.create_index([("_id",-1)],background=True)
#db.coll.ensureIndex({"homeid":1})
appToServer = {}
hardToServer = {}

def check_unique(str):
    '''checks whether the phone number of person is unique'''
    x = alive_user.find({"_id": str})
   # print type(x)
   # print x.alive
   
    if x.alive:
       # print "Unique"
        return 1
    else:
        return 0
def create_cookie(salt):
    ''' the cookie is composed of two parts : unique string +"."+ phone number '''
    # uuid is used to generate a random number
#    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode()).hexdigest()
def check_present(str):
    '''checks whether the phone number is registered '''
    x=alive_user.find({"_id":str})
    if x==None:
       # print "Not found"
        return 0
    else :
        return 1
        
def check_passlog(str1,str2):
    ''' checks whether the password has been entered correctly at login'''
    x=alive_user.find({"_id":str1},{"Password":str2})
    if x==None:
      #  print "Incorrect password"
        return 0
    else :
        return 1




def add_acookie(str1,str2):
    ''' for each and every login , this function adds the newly generated cookie to the user database and the home databases thus in
    effect updating all entries of the cookie '''
    part=str1.decode('utf8').split(".")
  #  print("new cookie"+str1)
    #x =alive_user.update({"_id":part[1]},{'$set':{"acookie":str1}},upsert=False)
    x=alive_user.find({"_id":part[1]},{"_id":0,"acookie":1})
    chk=x[0]["acookie"]
    chk.insert(0,str1)
  #  print str(str2)+"test"
    newcount=int(str2)+1
    x=alive_user.update({"_id":part[1]},{'$set':{"cookie_count":newcount}},upsert=False)
    x=alive_user.update({"_id":part[1]},{'$set':{"acookie":chk}},upsert=False)
    x=alive_user.find({"_id":part[1]},{"_id":0,"home_permanent_master":1})
    t=x[0]["home_permanent_master"]
    c=len(t)
    i=0
    while i<c:
        h=t[i]
        x=alive_home.update({"_id":h}, {'$set': {"permanent_persons_master.cookie":chk}},upsert=False)
        x=alive_home.update({"_id":h}, {'$set': {"permanent_persons_master.cookie_count":newcount}},upsert=False)
        i+=1
    x=alive_user.find({"_id":part[1]},{"_id":0,"home_permanent":1})
    t=x[0]["home_permanent"]
    c=len(t)
    i=0
    while i<c:
        h=t[i]
    #    print h 
        x=alive_home.find({"_id":h},{"_id":0,"permanent_persons_secondary":1})
     #   print x[0]
        count=x[0]["permanent_persons_secondary"]["Count"]
        j=1
        while j<=count:
            if x[0]["permanent_persons_secondary"][str(j)]["User_id_secondary"]==part[1]:
                p=alive_home.update({"_id":h},{'$set':{"permanent_persons_secondary."+str(j)+".cookie":chk}},upsert=False)
                p=alive_home.update({"_id":h},{'$set':{"permanent_persons_secondary."+str(j)+".cookie_count":newcount}},upsert=False)
                break
            j+=1
        i+=1




    '''x=alive_home.update({"permanent_persons_master.user_id":part[1]}, {'$set': {"permanent_persons_master.cookie":chk}},upsert=False)
    x=alive_home.update({"permanent_persons_master.user_id":part[1]}, {'$set': {"permanent_persons_master.cookie_count":newcount}},upsert=False)
    print x'''





def check_acookie(str1):
    '''checks whether the cookie entered is a valid cookie for the user '''
    part=str1.decode('utf8').split(".")
    x=alive_user.find({"_id":part[1]},{"acookie":1,"_id":0})  
    chk=x[0]["acookie"]
    count=0
    test=0
    x=alive_user.find({"_id":part[1]},{"cookie_count":1,"_id":0}) 
    chk1=x[0]["cookie_count"]
    while count<chk1:
        if chk[count] == str1:
           test=1
           break
        count+=1
    if test==1:
        return 1 
    elif test==0:
        return 0     

'''def find_homeid(str1):
    part=alive_user.find({"homeid":str1})
    if part ==None:
        return 0
    else :
       return part '''
def update_productdoc(prod_id,home_id,prod_type,prod_count,prod_cont):
    ''' this function will be used by software client to update the calues in the product document after the purchase and necessary installation of the product has been done '''
    x=alive_product.update({"_id":prod_id},{'$set':{"parent_home_id":home_id,"prod_type":prod_type}},upsert=False)
    list=prod_cont.split(".")
    if prod_type=="Slave":
                switch=[]
                count=0
                while count<int(prod_count):
                        
                        switch.append(list[count])
                        count+=1
                x=alive_product.update({"_id":prod_id},{'$set':{"No of switches":prod_count,"switch_types":switch}},upsert=False)

    if prod_type=="Master":
                slave=  []
                count=0
                while count <int(prod_count):
                        slave.append(list[count])
                        count+=1
                x=alive_product.update({"_id":prod_id},{'$set':{"No of slaves":prod_count,"slave_id":slave}},upsert=False)
def home_adduser_hubinc_cookie(str1,str2,str3):
    '''this function adds to each and every home document the permanent_master user '''
    x=alive_home.update({"_id":str1},{'$set':{"permanent_persons_master.user_id":str2}},upsert=False)
    x=alive_home.update({"_id":str1},{'$set':{"permanent_persons_master.hub_I_conc.hub_id":str3}},upsert=False)
    x=alive_user.find({"_id":str2},{"_id":0,"home_permanent_master":1})
    
    g=x[0]["home_permanent_master"]
    
    g.append(str1)

    x=alive_user.update({"_id":str2},{'$set':{"home_permanent_master":g}},upsert=False)
    x=alive_user.find({"_id":str2},{"_id":0,"acookie":1})
    chk=x[0]["acookie"]
    x=alive_home.update({"_id":str1}, {'$set': {"permanent_persons_master.cookie":chk}},upsert=False)
    y=alive_user.find({"_id":str2},{"_id":0,"cookie_count":1})
    chk1=y[0]["cookie_count"]
    x=alive_home.update({"_id":str1}, {'$set': {"permanent_persons_master.cookie_count":chk1}},upsert=False)
    x=alive_product.find({"_id":str3},{"_id":0,"slave_id":1})
    chk=x[0]["slave_id"]
    t=alive_product.find({"_id":str3},{"_id":0,"No of slaves":1})
    chk1=t[0]["No of slaves"]
    count=int(chk1)
    y=alive_home.update({"_id":str1},{'$set':{"permanent_persons_master.hub_I_conc.slave_id":chk}},upsert=False)
    i=0
    j=0
    p=0
    dic={}
    while i<count:
        switch={}
        kk=alive_product.update({"_id":chk[i]},{'$set':{"Master_Hub":str3}},upsert=False)
        z=alive_product.find({"_id":chk[i]},{"_id":0,"No of switches":1})
        j=int(z[0]["No of switches"])
        p=1
        while p<=j:
                switch[str(p)]=0
                p+=1
        
        dic[str(chk[i])]=switch
        i+=1
    hubi={}

    hubi[str(str3)]  =dic
    
    n=alive_home.update({"_id":str1},{'$set':{"Hub":hubi}},upsert=False)

def find_auth_user(cook,home_id,hub_i,slave_i):
    ''' This function find whether the cookie and hence the user has the rights to control the required slave id '''
    x=db.home.find({'_id':home_id})
    if x==None:
        return 0
    else :
        chk=x[0]["permanent_persons_master"]["hub_I_conc"]
        hub_id=chk["hub_id"]
        chk1=x[0]["permanent_persons_master"]["cookie"]
        st=cook.decode('utf8').split(".")
        i=x[0]["permanent_persons_master"]["cookie_count"]
        j=0
        while j<i:
            if hub_id==hub_i and chk1[j]==cook:
                return 1
            j+=1
        
        x=db.home.find({"_id":home_id},{"_id":0,"permanent_persons_secondary":1})
        #print x[0]
        count=x[0]["permanent_persons_secondary"]["Count"]
        j=1
        while j<=count:
            if x[0]["permanent_persons_secondary"][str(j)]["User_id_secondary"]==st[1]:
                l=x[0]["permanent_persons_secondary"][str(j)]["SlaveIDsList"]
                if (slave_i in l):
                    count=x[0]["permanent_persons_secondary"][str(j)]["cookie_count"]
                    chk2=x[0]["permanent_persons_secondary"][str(j)]["cookie"]
                    j1=0
                    while j1<count:
                        if chk2[j1]==cook:
                            return 1
                        j1+=1
            j+=1
        return 0




def cookie_counter(str1):
    ''' This just counts the number of cookies  against each user '''
    #print str1
    part=alive_user.find({"_id":str1})
    if part==None:
      # print "1st"
       return 1
    else :
        part=alive_user.find({"_id":str1},{"cookie_count":1,"_id":0})
     #   print "2nd"
      #  print str1
      #  print part[0]
        return part[0]["cookie_count"]

def change_state(home_id,hub_id,slave_id,swtch_no,new_state):
    ''' this func receiving data from the hardware client so as to change the data in the home doc'''
    s="Hub."+hub_id+"."+slave_id
  #  print s
    x=db.home.update({'_id':home_id},{'$set':{"Hub."+hub_id+"."+slave_id+"."+swtch_no:new_state}},upsert=False)
    if x==None:
        return 0
    else :
        return 1 

    
        
        
        

           
def check_password(str):
    u = 0
    l = 0
    n = 0
    if ' ' in str :
       # print "Password cannot contain whitespaces"
        return 0
    length = len(str)
    for i in str :
         if i.isdigit() :
            n = n+1
            continue
         if i.isupper() :
            u = u+1
            continue
         if i.islower() :
            l = l+1
    if u==0 :
        print "Password must contain at least one Upper case letter"
        return 0
    if l==0 :
        print "Password must contain at least one Lower case letter"
        return 0
    if n==0 :
        print "Password must contain at least one Numberic digit"
        return 0
    return 1
def add_newuser_slaveid(str1,str2,str3):
    ''' this function is used to add limited access control to certain users ( they are permanent)'''
    k=0
    x=alive_home.find({"_id":str1},{"_id":0,"permanent_persons_secondary.Count":1})
   
    cnt=x[0]["permanent_persons_secondary"]
    cont=cnt["Count"]
    count=int(cont)
   # print count 
   # print "count :" +str(count)
    part=str3.decode('utf8').split(".")
    hubi={}
    hubi['User_id_secondary']=str2
    hubi['SlaveIDsList']=part
    x=alive_user.find({"_id":str2},{"_id":0,"acookie":1})
    chk=x[0]["acookie"]
    hubi['cookie']=chk
    y=alive_user.find({"_id":str2},{"_id":0,"cookie_count":1})
    chk1=y[0]["cookie_count"]
    hubi['cookie_count']=chk1
  #  print "hubi :\n"
  #  print hubi

    pos=count+1
  #  print "pos:" +str(pos)
    x=alive_home.update({"_id":str1},{'$set':{"permanent_persons_secondary."+str(pos):hubi}},upsert=False)
    if x==None:
        k=1
    x=alive_home.update({"_id":str1},{'$set':{"permanent_persons_secondary.Count":pos}},upsert=False)
    if x==None :
        k=1
    x=alive_user.find({"_id":str2},{"home_permanent":1,"_id":0})
  #  print x[0]
    l=x[0]["home_permanent"]
    l.append(str1)
    x=alive_user.update({"_id":str2},{'$set':{"home_permanent":l}},upsert=False)
    if x==None:
        k=1
    if k==0:
        return 1
    elif k==1:
        return 0

    
    
    
    
   

    

def remove_user(str1,str2):
    '''removes the limited access control users by cookie , hub , phone number '''
    k=0
    x=alive_home.find({"_id":str1},{"_id":0,"permanent_persons_secondary.Count":1})
    cnt=x[0]["permanent_persons_secondary"]
    count=cnt["Count"]
    i=1
    while i<=count:
        x=alive_home.find({"_id":str1},{"_id":0,"permanent_persons_secondary."+str(i):1})
        j=x[0]["permanent_persons_secondary"]
        d=j[str(i)]
        if d['User_id_secondary']==str2:
            break
        i+=1
    x=alive_home.update({"_id":str1},{'$unset':{"permanent_persons_secondary."+str(i):1}})
   # print k
    if x==None:
        k=1
   # print k
    count-=1
    x=alive_home.update({"_id":str1},{'$set':{"permanent_persons_secondary.Count":count}},upsert=False)
    if x==None:
        k=1
   # print k
    x=alive_user.find({"_id":str2},{"_id":0,"home_permanent":1})
    l=x[0]["home_permanent"]
    p=0
    k1=len(l)
    while p<k1:
        if l[p]==str1:
            l.remove(str1)

            x=alive_user.update({"_id":str2},{'$set':{"home_permanent":l}},upsert=False)
            break
            if x==None:
                k=1
            
        p+=1
    if k==1:
        return 0
    elif k==0:
        return 1


    









def find_object(str):
    ''' checks whether a connection instance is still active '''
    if str in appToServer:
            return 1 
    elif  check_acookie(str)==1: 
            return 0
    else :
        return 2
def remove_cookie(str1):
    '''deleted the current session and cookie corressponding to it from the database and also removes it from the apptoserver dictionary'''
    if str1 in appToServer:
        del appToServer[str1]
    part=str1.decode('utf8').split(".")
    x=alive_user.find({"_id":part[1]},{"_id":0,"acookie":1})
    chk=x[0]["acookie"]
    
    chk.remove(str1)
    newcount=cookie_counter(part[1])-1
    x=alive_user.update({"_id":part[1]},{'$set':{"cookie_count":newcount}},upsert=False)
    x=alive_user.update({"_id":part[1]},{'$set':{"acookie":chk}},upsert=False)
    x=alive_user.find({"_id":part[1]},{"_id":0,"home_permanent_master":1})
    t=x[0]["home_permanent_master"]
    c=len(t)
    i=0
    while i<c:
        h=t[i]
        x=alive_home.update({"_id":h}, {'$set': {"permanent_persons_master.cookie":chk}},upsert=False)
        x=alive_home.update({"_id":h}, {'$set': {"permanent_persons_master.cookie_count":newcount}},upsert=False)
        i+=1
    x=alive_user.find({"_id":part[1]},{"_id":0,"home_permanent":1})
    t=x[0]["home_permanent"]
    c=len(t)
    i=0
    while i<c:
        h=t[i]
        x=alive_home.find({"_id":h},{"_id":0,"permanent_persons_secondary":1})
        count=x[0]["permanent_persons_secondary"]["Count"]
        j=1
        while j<=count:
            if x[0]["permanent_persons_secondary"][str(j)]["User_id_secondary"]==part[1]:
                p=alive_home.update({"_id":h},{'$set':{"permanent_persons_secondary."+str(j)+".cookie":chk}},upsert=False)
                p=alive_home.update({"_id":h},{'$set':{"permanent_persons_secondary."+str(j)+".cookie_count":newcount}},upsert=False)
                break
            j+=1
        i+=1

def find_status(home_id,master_id):
    ''' used to return the present status of switches in   the home doc'''
    x=alive_home.find({"_id":home_id },{"permanent_persons_master":1,"_id":0})
    k=x[0]["permanent_persons_master"]["user_id"]
    if k==master_id:
        p=alive_home.find({"_id":home_id },{"Hub":1,"_id":0})
        obj=p[0]["Hub"]
        return obj
    else :
        return None

            

   


class MyServerProtocol(WebSocketServerProtocol):
    
    
   
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        print factory.countConnections 
    
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        list = payload.decode('utf8').split("-")
        print payload
        if list [0]=="C" and list [1]=="H1":
            ''' communicates with the software client and initialises the home document to bare essential values'''
            home_id=list[2]
            home_pin=list[3]
            home_address=list[4]
            post={"_id":home_id,"home_pin":home_pin,"home_address":home_address,"permanent_persons_master":{"user_id":"","hub_I_conc":{"hub_id":""},"cookie":[]},"permanent_persons_secondary":{"Count":0}}        
            post_id = alive_home.insert_one(post).inserted_id    
        if list[0]=="C" and list[1]=="H2":
            '''communicates with the software client and add the master user to the home document'''
            home_id=list[2]
            user_id=list[3]
            hub_I_conc=list[4]
            home_adduser_hubinc_cookie(list[2],list[3],list[4])
        if list[0]=="C"and list[1]=="P":
            '''communicates with the software client and initialises the product document'''
            prod_id=list[2]
            prod_type=list[3]
            if prod_type=="s":
                '''switch=[]
                prod_count=list[4]
                count=1
                while count<=int(prod_count):
                        switch.append(list[4+count])
                        count+=1'''
                post={"_id":prod_id,"parent_home_id":"","prod_type":"Slave"}
            if prod_type=="m":
                '''prod_count=list[4]  
                slave=  []
                count=1
                while count <=int(prod_count):
                    slave.append(list[4+count])
                    count+=1'''
                post={"_id":prod_id,"parent_home_id":"","prod_type":"Master"}
            post_id = alive_product.insert_one(post).inserted_id
        if list[0]=="C" and list[1]=="H":
            '''communicates with the software client and upgrades the product doc'''
            prod_id=list[2]
            home_id=list[3]
            prod_type=list[4]
            prod_count=list[5]
            prod_cont=list[6]
            if prod_type=="m":
                prod_type="Master"
            if prod_type=="s":
                prod_type="Slave"
            update_productdoc(prod_id,home_id,prod_type,prod_count,prod_cont)      

        if list[1] == "A" and list[0]=="A":
        
            if check_unique(list[3]):  
                if check_password(list[4])==0:
                  self.sendMessage("S-R-0-Password has incorrect format", isBinary)
                  return 
                salt=str(int(time.time()*1000))
                cook = create_cookie(salt)
                cooki=cook+"."+list[3]
                cookiec=1
                cookie=[]
                cookie.append(cooki)
                servcookR="S-R-C-"+cookie[0]
                appToServer[cooki]=self
                '''count_perm=list[12]
                count=1
                '''
                home_permanent_masterid=[]
                
                '''
                while count<=int(count_perm):
                      home_permanent_masterid.append(list[12+count]) 
                      count+=1
                newcount=12+count
                count_temp=list[newcount]
                count=1
                '''
                home_temporaryid=[]
                '''
                while count<=int(count_temp):
                        newcount+=1
                        home_temporaryid.append(list[newcount])
                        count+=1
                '''
                home_permanent=[]
                #user_metadata={"email address":list[4],"User's Name":list[2],"Sex":list[6],"DOB":list[7],"UID":list[8],"mobile":list[3],"initial_address,":list[9],"coordinate":{"location_longitude":list[10],"location_latitude":list[11]}}
                user_metadata={"email address":list[5],"User's Name":list[2],"Sex":list[6],"DOB":list[7],"UID":list[8],"mobile":list[3]}
                post = {"User's Name": list[2], "_id": list[3], "user_metadata":user_metadata , "password":list[4],"acookie":cookie,"cookie_count":cookiec,"home_permanent":home_permanent,"home_permanent_master":home_permanent_masterid,"home_temporary":home_temporaryid}

                post_id = alive_user.insert_one(post).inserted_id
               
                self.sendMessage(u"S-R-1-New Registration successful".encode('utf8'))
                
                self.sendMessage(servcookR.encode('utf8'))
                
                
            else:
                self.sendMessage(u"S-R-0-Already registered".encode('utf8'))   
               
        
        if list[1]=="B" and list[0]=="A":
           if check_present(list[2]):
                if check_passlog(list[2],list[3])==0:
                    self.sendMessage("S-J-ERROR_CODE",isBinary)
                    return
                else :

                    salt=str(int(time.time()*1000))
                    cook = create_cookie(salt)
                    cook1=cook+"."+list[2]
                    cookie_count=cookie_counter(list[2])
                    #print "presentcook"+str(cookie_count)
                    add_acookie(cook1,cookie_count) 
                    self.sendMessage(u"S-J-SUCCESS".encode('utf8'))

                    servcookL="S-L-C-"+cook1
                    appToServer[cook1]=self
                   
                    self.sendMessage(servcookL.encode('utf8'))
        if list[0]=="A" and list[1]=="C":
            if find_object(list[2])== 0:
                appToServer[list[2]]=self
                #print list 
            test=find_auth_user(list[2],list[3],list[4],list[5])
            if test==1:
                print "Authenticated"
                strk="8-S-W-"+list[3]+"-"+list[4]+"-"+list[5]+"-"+list[6]+"-"+list[7]+"-"
                #print strk
                hardToServer[list[5]].sendMessage(strk.encode('utf8'))
                #change_state(list[3],list[4],list[5],list[6],list[7])
            elif test==0:
                print "Not found/Authenticated"
        if list[0]=="A" and list [1]=="D":
            remove_cookie(list[2])
        if list[0]=="A" and list [1]=="E":
            if check_acookie(list[2])==1:
               # print "success"
                k=add_newuser_slaveid(list[3],list[4],list[5])
                if k==1:
                    self.sendMessage(u"S-K-SUCCESS".encode('utf8'))
                elif k==0:
                    self.sendMessage(u"S-K-ERROR_CODE".encode('utf8'))
        if list[0]=="A"and list[1]=="F":
             if check_acookie(list[2])==1:
                k=remove_user(list[3],list[4])
                if k==1:
                    self.sendMessage(u"S-K-SUCCESS".encode('utf8'))
                elif k==0:
                    self.sendMessage(u"S-K-ERROR_CODE".encode('utf8'))
        if list[0]=="A" and list[1]=="G":
                k=find_status(list[2],list[3])
                #print type(k)
                json = demjson.encode(k)
                #print type(json)
                spg="S-H-"+list[2]+"-"+list[3]+"-"+json
                self.sendMessage(spg.encode('utf8'))








        if list[0]=="H" and list[1]=="S":
            hardToServer[list[2]]=self
        if list[0]=="H" and list[1]=="T": 
                k=change_state(list[2],list[3],list[4],list[5],list[6])
                if k==1:
                    hardToServer[list[3]].sendMessage(u"4-S-V-SUCCESS-".encode('utf8'))
                if k==0:
                    hardToServer[list[3]].sendMessage(u"4-S-V-ERROR-".encode('utf8'))


        
      
      
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol
    factory.setProtocolOptions(autoPingInterval=100,autoPingTimeout=50)
  

    reactor.listenTCP(9000, factory)
    reactor.run()