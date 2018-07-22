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


delay_timeout = 1
server_sock = socket
client_sock = socket


def create_server(ipaddr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ipaddr, int(port))
    sock.bind(server_address)
    return sock


def wait_connection(sock, clients=1):
    global client_sock
    sock.listen(clients)
    client_sock, _ingnore = sock.accept()


def recv_msg(client_connection):
    data = client_connection.recv(128)
    return data.decode('utf-8')


def is_cmd(cmd_one, cmd_req):
    if cmd_one[:len(cmd_req)] == cmd_req:
        return True, cmd_one[len(cmd_req) + 1:]
    return False, ""


def send_message(connection, message):
    print("send: %s" % message)
    connection.sendall(message.encode())


def recv_message(connection):
    print("recv: %s" % connection.recv(128).decode("utf-8"))


def do_cmd(cmd_line):
    global server_sock
    global client_sock
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
            server_sock = create_server('localhost', num_port)
            print("server started")
        elif server_opt == cmd_opt_close_server:
            server_sock.close()
            print("server closed")
        else:
            print("invalid option for --server %s" % server_opt)

    if is_send_msg:
        send_message(client_sock, msg)
        recv_message(client_sock)

    if is_wait_conn:
        wait_connection(server_sock, 1)
    # ---------------- end -----------------

    return False


def main():
    while True:
        cmd_line = input("please type command: ")
        is_exit = do_cmd(cmd_line)
        if is_exit:
            break


main()
