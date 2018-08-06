import socket
import threading
from time import sleep


def init_client(portnum):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', int(portnum)))
    return client_sock


def revert(inputstr):
    res = ""
    for ch in inputstr:
        res = ch + res

    return res


def main(portnum, it):

    client_sock = init_client(portnum)
    while True:
        data = client_sock.recv(60000)
        if len(data) == 0:
            print("server is closed")
            break
        strmsg = str(data.decode("utf-8"))
        print("id:[%s], packet sz:[%s bytes]" % (str(it), str(len(strmsg))))
        responceStr = revert(strmsg)
        client_sock.sendall(responceStr.encode())
        sleep(0.05)


def start_client_impl(port_num, it):
    thr = threading.Thread(target=main, args=(port_num, it))
    thr.start()


def test_perf():
    count_clients = 1 # int(input("enter please count clients: "))
    port_num = 1234 # str(input("server port: "))
    it = 0
    while it < count_clients:
        start_client_impl(port_num, it)
        it += 1


test_perf()