import socket
import dnslib
from dnslib import QTYPE


def Find_IP(input_qname, DCmessage):
    qname = str(input_qname)
    
    qnamelist = qname.split(".")
    qnamelist.pop(len(qnamelist) - 1) 
    for i in range(0, len(qnamelist)):
        qnamelist[i] = qnamelist[i] + "."
    qnamelist.reverse() 
    root_server = '198.41.0.4'
    ip_tmp = root_server
    domain = ""
    for i in qnamelist:
        domain = i + domain
        print(ip_tmp)
        r = dnslib.DNSRecord.question(domain)
        rr = r.send(root_server)
        ServerReply = dnslib.DNSRecord.parse(rr)
        # print(res)

        if (ServerReply.auth != []):
            root_server = ServerReply.auth[0].rdata.__str__()
            if (ServerReply.ar != []):
                ip_tmp = ServerReply.ar[0].rdata.__str__()
            else:
                Find_IP(ServerReply.auth[0].rdata, DCmessage)
        if ((ServerReply.auth == []) and (ServerReply.rr != [])):
            if (str(ServerReply.rr[0].rdata)[0].isdigit() == True):
                continue
            else:
                for RR in ServerReply.rr:
                    DCmessage.add_answer(RR)
                ServerReply = Find_IP(ServerReply.rr[0].rdata, DCmessage)
    return ServerReply

def Local_DNS(flag):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    serverSocket.bind(("127.0.0.1",1234))
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    IP_cache={}  #cache[qname]=responseMessage
    
    while True:
        message, clinetAddress = serverSocket.recvfrom(2048)
        message_P = dnslib.DNSRecord.parse(message)
        Identifier =  str(message_P.q.qname) + "|" + QTYPE[message_P.q.qtype]

        if(Identifier in IP_cache): #have already searched before and find in cache!
            rr = IP_cache[Identifier]
            DCmessage = message_P.reply()
            for RR in rr:
                DCmessage.add_answer(RR)
        else:
            if(flag == 0):
                request = message_P.send("223.5.5.5")
                DCmessage = dnslib.DNSRecord.parse(request)
            else:
                DCmessage = message_P.reply()
                ServerReply = Find_IP(message_P.q.qname, DCmessage)
                
                for RR in ServerReply.rr:
                    DCmessage.add_answer(RR)

        DCmessage.header.rd = 1
        IP_cache[Identifier] = DCmessage.rr
        serverSocket.sendto(DCmessage.pack(),clinetAddress)
        print("===========================")


if __name__ == '__main__':
    try:
        # flag = int(sys.argv[1])
        flag = 1
        Local_DNS(flag)
    except KeyboardInterrupt:
        pass

# serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# serverSocket.bind(("127.0.0.1",1234))
# clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# IP_cache={}  #cache[qname]=responseMessage
# root_server = '198.41.0.4'
# flag=1

# while True:      
#     message, clinetAddress = serverSocket.recvfrom(2048)
#     message_P = dnslib.DNSRecord.parse(message)
#     Identifier =  str(message_P.q.qname) + "|" + QTYPE[message_P.q.qtype]

#     if(Identifier in IP_cache): #have already searched before and find in cache!
#         rr = IP_cache[Identifier]
#         DCmessage = message_P.reply()
#         for RR in rr:
#             DCmessage.add_answer(RR)
#     else:
#         if(flag == 0):
#             request = message_P.send("223.5.5.5")
#             DCmessage = dnslib.DNSRecord.parse(request)
#         else:
#             request = message_P.send(root_server)
#             print(root_server)
#             DCmessage = message_P.reply()
#             ServerReply = dnslib.DNSRecord.parse(request)
#             qname = message_P.q.qname

#             break_flag= False
#             while(not (ServerReply.rr!=[] and QTYPE[ServerReply.rr[0].rtype] == "A")):
#                 if(ServerReply.rr==[]):
#                     for i in range(ServerReply.auth.__len__()):
#                         if (i != ServerReply.auth.__len__()-1):
#                             try:
#                                 request2 = dnslib.DNSRecord.question(qname).send(str(ServerReply.auth[i].rdata))
#                                 if(ServerReply.ar != []):
#                                     print(ServerReply.ar[i].rdata)
#                                 else:
#                                     print(ServerReply.auth[i].rdata)
#                                 break
#                             except:
#                                 continue
#                         else:
#                             try:
#                                 request2 = dnslib.DNSRecord.question(qname).send(str(ServerReply.auth[i].rdata))
#                                 if(ServerReply.ar != []):
#                                     print(ServerReply.ar[i].rdata)
#                                 else:
#                                     print(ServerReply.auth[i].rdata)
#                                 break
#                             except:
#                                 break_flag = True
#                                 break
#                     if (break_flag == True):
#                         break;
#                     ServerReply = dnslib.DNSRecord.parse(request2)
#                 elif(QTYPE[ServerReply.rr[0].rtype] != "A"):
#                     for RR in ServerReply.rr:
#                         DCmessage.add_answer(RR)
#                     qname=str(ServerReply.rr[0].rdata)
#                     request2=dnslib.DNSRecord.question(qname).send(root_server)
#                     print(root_server)
#                     ServerReply = dnslib.DNSRecord.parse(request2)
#             for RR in ServerReply.rr:
#                 DCmessage.add_answer(RR)

#     IP_cache[Identifier] = DCmessage.rr
#     serverSocket.sendto(DCmessage.pack(),clinetAddress)