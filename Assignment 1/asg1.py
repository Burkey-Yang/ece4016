# -*- coding: UTF-8 -*-

import socket
import dnslib
from dnslib import QTYPE
import sys

def query(qin, dcm):
    qname = str(qin)
    
    qnamelist = qname.split(".")
    qnamelist.pop(len(qnamelist) - 1) 
    for i in range(0, len(qnamelist)):
        qnamelist[i] = qnamelist[i] + "."
    qnamelist.reverse() 
    a = '198.41.0.4'
    ip_tmp = a
    domain = ""
    for i in qnamelist:
        domain = i + domain
        print(ip_tmp)
        r = dnslib.DNSRecord.question(domain)
        rr = r.send(a)
        res = dnslib.DNSRecord.parse(rr)
        # print(res)

        if (res.auth != []):
            a = res.auth[0].rdata.__str__()
            if (res.ar != []):
                ip_tmp = res.ar[0].rdata.__str__()
            else:
                query(res.auth[0].rdata, dcm)
        if ((res.auth == []) and (res.rr != [])):
            if (str(res.rr[0].rdata)[0].isdigit() == True):
                continue
            else:
                for RR in res.rr:
                    dcm.add_answer(RR)
                res = query(res.rr[0].rdata, dcm)
    return res

def local_DNS_Server(flag):
    cache = {}
    while True:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('127.0.0.1', 1234))
        message, clientAddress = serverSocket.recvfrom(2048)
        message_parse = dnslib.DNSRecord.parse(message)
        message_parse.header.set_rd(0)
        message = dnslib.DNSRecord.pack(message_parse)
        qname =  str(message_parse.q.qname)

        if message_parse.q.qname in cache:
            rr = cache[qname]
            DCmessage = message_parse.reply()
            for RR in rr:
                DCmessage.add_answer(RR)
        else: 
            if flag == 0:
                request = message_parse.send("223.5.5.5")
                DCmessage = dnslib.DNSRecord.parse(request)
            else:
                DCmessage = message_parse.reply()
                res = query(message_parse.q.qname, DCmessage)
                
                for RR in res.rr:
                    DCmessage.add_answer(RR)
            
            DCmessage.header.rd = 1
            cache[qname] = DCmessage.rr
            serverSocket.sendto(DCmessage.pack(),clientAddress)
        print("===========================")


if __name__ == '__main__':
    try:
        # flag = int(sys.argv[1])
        flag = 1
        local_DNS_Server(flag)
    except KeyboardInterrupt:
        pass
