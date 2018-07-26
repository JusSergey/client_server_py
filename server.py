import socket
from time import sleep


cmd_server = "--server"
cmd_port = "--port"
cmd_exit = "--exit"
cmd_msg = "--msg"
cmd_wait_conn = "--wait_conn"
cmd_opt_close_server = "close"
cmd_opt_start_server = "start"
cmd_help = "--help"


class server:
    def __init__(self, port, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.clients = list()
        self.count = 0
        self.ip = ip

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


serv_sock = server


def is_cmd(cmd_one, cmd_req):
    if cmd_one[:len(cmd_req)] == cmd_req:
        return True, cmd_one[len(cmd_req) + 1:]
    return False, ""


def do_cmd(cmd_line):
    global serv_sock
    is_server = False
    server_opt = ""
    num_port = ""
    is_send_msg = False
    msg = ""
    is_wait_conn = False
    cmd_list = cmd_line.split(" ")

    for cmd_one in cmd_list:
        # exit
        if cmd_one == "--exit":
            return True;
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
            serv_sock = server(int(num_port), "localhost")
            serv_sock.create()
            print("server started")

        elif server_opt == cmd_opt_close_server:
            serv_sock.close()
            print("server closed")

        else:
            print("invalid option for --server %s" % server_opt)

    if is_send_msg:
        serv_sock.send_msg(msg, 0)
        data = serv_sock.receive_msg(0, 128)
        print(data.decode("utf-8"))

    if is_wait_conn:
        serv_sock.listen(1)
        serv_sock.wait_connection()
    # ---------------- end -----------------

    return False


def main():
    while True:
        cmd_line = input("please type command: ")
        is_exit = do_cmd(cmd_line)
        if is_exit:
            break


main()
