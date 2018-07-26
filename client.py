import socket
from time import sleep

client_sock = ""


def init_client(portnum):
    global client_sock
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', int(portnum)))


def revert(inputstr):
    res = ""
    for ch in inputstr:
        res = ch + res

    return res


def main():
    portnum = "12300"

    init_client(portnum)
    while True:
        data = client_sock.recv(128)
        strmsg = str(data.decode("utf-8"))
        print("receive:  %s" % strmsg)
        responceStr = revert(strmsg)
        print("responce: %s" % responceStr)
        client_sock.sendall(responceStr.encode())
        sleep(1)


main()