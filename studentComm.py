import socket
import json
import studentcodeExample as studentcode

# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_CLOEXEC)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind(('localhost', 6000))
ss.listen(10)
print('Waiting for simulator')

(clientsocket, address) = ss.accept()


def recv_commands():
    message = ""


    while(1):
        messagepart = clientsocket.recv(2048).decode()

        message += messagepart
        if message[-1] == '\n':


            jsonargs = json.loads(messagepart)
            message = ""

            if(jsonargs["exit"] != 0):
                return

            #todo: json data sanitization
            bitrate = studentcode.student_entrypoint(jsonargs["Measured Bandwidth"], jsonargs["Previous Throughput"], jsonargs["Buffer Occupancy"], jsonargs["Available Bitrates"], jsonargs["Video Time"], jsonargs["Chunk"], jsonargs["Rebuffering Time"], jsonargs["Preferred Bitrate"])

            payload = json.dumps({"bitrate" : bitrate}) + '\n'
            clientsocket.sendall(payload.encode())







if __name__ == "__main__":

    recv_commands()
    ss.close()
