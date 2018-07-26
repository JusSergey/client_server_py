import socket
import random
import threading
import string
from time import sleep


cmd_server = "--server"
cmd_port = "--port"
cmd_exit = "--exit"
cmd_msg = "--msg"
cmd_msg_dump = "--msg_dump"
cmd_wait_conn = "--wait_conn"
cmd_opt_close_server = "close"
cmd_opt_start_server = "start"
cmd_help = "--help"
cmd_repeat = "--repeat"
cmd_alias_server_start = ("--aserver", "--server=start --port=12300 --wait_conn")


class Server:
    def __init__(self, port, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.clients = list()
        self.scheduler_task = threading.Thread
        self.count = 0
        self.ip = ip
        self.running_task = False
        self.status_scheduler = False
        self.dump_data = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(60000)])

    def create(self):
        self.sock.bind((self.ip, self.port))
        return self.sock

    def listen(self, count):
        self.sock.listen(count)

    def wait_connection(self):
        self.clients.append(self.sock.accept()[0])
        self.count += 1

    def receive_msg(self, id_client, size):
        return self.clients[id_client].recv(size)

    def send_msg(self, message, id_client):
        self.clients[id_client].sendall(message.encode())

    def close(self):
        self.sock.close()

    def size(self):
        return self.count

    def task_repeater(self, cmd_line, repeat_count):
        print("rask repeater")
        i = repeat_count
        self.running_task = True
        self.status_scheduler = True
        while self.running_task and (repeat_count == 0 or i > 0):
            do_cmd(cmd_line)
            i -= 0
        self.status_scheduler = False

    def schedule_task(self, cmd_line, repeat_count):
        self.scheduler_task = threading.Thread(target=self.task_repeater, args=(cmd_line, repeat_count))
        self.scheduler_task.start()

    def stop_scheduler(self):
        self.running_task = False
        while self.status_scheduler:
            sleep(0.01)


serv_sock = Server


def is_cmd(cmd_one, cmd_req):
    if cmd_one[:len(cmd_req)] == cmd_req:
        return True, cmd_one[len(cmd_req) + 1:]
    return False, ""


def do_cmd(cmd_line):
    print("do cmd %s" % cmd_line)
    global serv_sock
    is_server = False
    is_msg_dump = False
    server_opt = ""
    num_port = ""
    is_send_msg = False
    msg = ""
    is_wait_conn = False
    cmd_list = cmd_line.split(" ")

    if len(cmd_list) > 0 and cmd_list[0] == cmd_repeat:
        print("in if")
        serv_sock.schedule_task(cmd_line[len(cmd_repeat)+1:], 0)
        return

    for cmd_one in cmd_list:
        # exit
        if cmd_one == "--exit":
            return True
        # send auto-generated msg
        elif cmd_one == cmd_msg_dump:
            is_msg_dump = True
        # server
        elif is_cmd(cmd_one, cmd_server)[0]:
            server_opt = is_cmd(cmd_one, cmd_server)[1]
            is_server = True
        # port
        elif is_cmd(cmd_one, cmd_port)[0]:
            num_port = is_cmd(cmd_one, cmd_port)[1]
        # send message
        elif is_cmd(cmd_one, cmd_msg)[0]:
            is_send_msg = True
            msg = is_cmd(cmd_one, cmd_msg)[1]
        # help
        elif cmd_one == cmd_help:
            print("%s=<start|close>, %s=<num_port>, %s, %s=<your text>, %s, %s" % (cmd_server, cmd_port, cmd_exit, cmd_msg, cmd_wait_conn, cmd_help))
        # wait connection
        elif cmd_one == cmd_wait_conn:
            is_wait_conn = True
        else:
            print("unknown cmd %s" % cmd_one)

    # --------- doing select cmd -----------
    if is_server:
        if server_opt == cmd_opt_start_server and num_port == "":
            print("please enter port, and repeat.")

        elif server_opt == cmd_opt_start_server:
            serv_sock = Server(int(num_port), "localhost")
            serv_sock.create()
            print("server started")

        elif server_opt == cmd_opt_close_server:
            serv_sock.close()
            print("server closed")

        else:
            print("invalid option for --server %s" % server_opt)

    if is_send_msg:
        serv_sock.send_msg(msg, 0)
        data = serv_sock.receive_msg(0, len(msg))
        print(data.decode("utf-8"))

    if is_msg_dump:
        serv_sock.send_msg(serv_sock.dump_data, 0)
        data = serv_sock.receive_msg(0, len(serv_sock.dump_data))
        print(data.decode("utf-8"))

    if is_wait_conn:
        serv_sock.listen(1)
        serv_sock.wait_connection()
    # ---------------- end -----------------

    return False


def main():
    while True:
        cmd_line = input("please type command: ")
        if cmd_line == cmd_alias_server_start[0]:
            cmd_line = cmd_alias_server_start[1]

        is_exit = do_cmd(cmd_line)
        if is_exit:
            break


main()
