import socket
import threading
from time import sleep

client_sock = socket

cmd_repeat = "--repeat"
cmd_msg = "--msg"
cmd_close = "--close"


def init_client(portnum):
    global client_sock
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', int(portnum)))


def revert(inputstr):
    res = ""
    for ch in inputstr:
        res = ch + res

    return res


def is_cmd(cmd_one, cmd_req):
    if cmd_one[:len(cmd_req)] == cmd_req:
        return True, cmd_one[len(cmd_req) + 1:]
    return False, ""


def send_message(connection, message):
    print("send: %s" % message)
    connection.sendall(message.encode())


def recv_msg(client_connection):
    data = client_connection.recv(128)
    return data.decode('utf-8')


def do_cmd(cmd_line):
    global client_sock
    is_repeat = False
    is_send = False
    is_close = False
    count_repeat = ""
    snd_msg = ""
    cmd_list = cmd_line.split(" ")
    for cmd_one in cmd_list:
        if is_cmd(cmd_one, cmd_repeat)[0]:
            count_repeat = is_cmd(cmd_one, cmd_repeat)[1]
            if count_repeat == "":
                count_repeat = "0"
        if is_cmd(cmd_one, cmd_msg)[0]:
            snd_msg = is_cmd(cmd_one, cmd_msg)[1]
            is_send = True
        if cmd_line == cmd_close:
            is_close = True

    i = 0
    step = 0
    max_val = 1

    if is_repeat and int(count_repeat) > 0:
        i = 0
        step = 1
        max_val = int(count_repeat)
    elif count_repeat != "0":
        i = 0
        step = 1
        max_val = 1

    print("%d, %d, %d" % (i, max_val, step))

    while i < max_val:
        if is_send:
            send_message(client_sock, snd_msg)
        if is_close:
            client_sock.close()
        i += step
        sleep(1)


def read_socket_():
    global client_sock
    while True:
        print("recv: %s" % recv_msg(client_sock))


def main():
    portnum = "12300"

    init_client(portnum)
    thr_recv = threading.Thread(target=read_socket_, args=())
    thr_recv.start()
    while True:
        cmd_line = input("$: ")
        do_cmd(cmd_line)


main()