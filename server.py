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
cmd_tm = "--timeout"
cmd_delay = "--delay"
cmd_repeat = "--repeat"
сmd_dispersion = "--dispersion"
cmd_alias_server_start = ("--aserver", "--server=start --port=1235")


class Server:
    def __init__(self, port, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.clients = list()
        self.thr = list()
        self.scheduler_task = threading.Thread
        self.count = 0
        self.ip = ip
        self.running_task = False
        self.status_scheduler = False
        self.dump_data = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(60000)])
        self.enable_print = True

    def set_enable_print(self, is_enable):
        self.enable_print = is_enable

    def create(self):
        self.sock.bind((self.ip, self.port))
        return self.sock

    def listen(self, count):
        self.sock.listen(count)

    def rea(self, fd_c):
        while True:
            sleep(0.01)
            data = self.clients[fd_c].recv(60000)
            if len(data) == 0:
                pass
            elif self.enable_print:
                print("id:[%d] packet sz: [%s]" % (fd_c, str(len(data.decode("UTF-8")))))

    def wait_connection(self):
        cli_fd = self.sock.accept()
        self.clients.append(cli_fd[0])
        curr_count_c = self.count
        self.count += 1
        thr_local = threading.Thread(target=self.rea, args=(curr_count_c,))
        thr_local.start()
        print("accepted client...")

    def receive_msg(self, id_client, size):
        return self.clients[id_client].recv(size)

    def send_msg(self, message, id_client):
        self.clients[id_client].sendall(message.encode())

    def close(self):
        self.sock.close()

    def size(self):
        return self.count

    def task_repeater(self, cmd_line, repeat_count):
        print("task repeater")
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

    def init_acceptor(self):
        print("init acceptor")
        thr_local = threading.Thread(target=self.init_acceptor_impl, args=())
        thr_local.start()
        self.thr.append(thr_local)

    def init_acceptor_impl(self):
        while True:
            print("waiting...")
            self.listen(666)
            self.wait_connection()


ARG = 0
CMD = 1
THR = 2


data_init = [(cmd_server, True),
             (cmd_port, True),
             (cmd_exit, False),
             (cmd_msg, True),
             (cmd_msg_dump, False),
             (cmd_help, False),
             (cmd_tm, True),
             (cmd_delay, True),
             (cmd_repeat, False),
             (сmd_dispersion, True),
             (cmd_repeat, False)]


class CommandContext:
    def __init__(self):
        self.do_server = [False, str()]
        self.do_message = [False, str()]
        self.do_message_dump = [False, str()]
        self.do_help = [False, str()]
        self.do_delay = [False, str(), float(0)]
        self.do_timeout = [False, str()]
        self.do_exit = [False, str()]
        self.do_repeat = [False, str()]
        self.opt_delay = [False, str()]
        self.opt_timeout = [False, str()]
        self.opt_message = [False, str()]
        self.opt_server = [False, str()]
        self.opt_port = [False, str()]
        self.opt_dispersion = [False, str()]


class DoCmd:
    def __init__(self, cmd, serv_sock_):
        self.cmds = cmd.split(" ")
        self.context = CommandContext()
        self.serv_sock = serv_sock_
        self.parse()


    def check(self, cmd):
        line = cmd.split("=")
        finded = False
        for arg in data_init:
            if arg[0] == line[0] and (len(line) > 0 and arg[1]):
                finded = True

        return finded

    def get_field(self, field_cmd_raw, assign_value):
        field_cmd = field_cmd_raw.split("=")[0]
        if field_cmd == cmd_server:
            self.context.do_server = assign_value
        if field_cmd == cmd_port:
            self.context.opt_port = assign_value
        if field_cmd == cmd_exit:
            self.context.do_exit = assign_value
        if field_cmd == cmd_msg:
            self.context.do_message = assign_value
        if field_cmd == cmd_msg_dump:
            self.context.do_message_dump = assign_value
        if field_cmd == cmd_help:
            self.context.do_help = assign_value
        if field_cmd == cmd_tm:
            self.context.opt_timeout = assign_value
        if field_cmd == cmd_delay:
            self.context.do_delay = assign_value
        if field_cmd == cmd_repeat:
            self.context.do_repeat = assign_value
        if field_cmd == сmd_dispersion:
            self.context.opt_dispersion = assign_value

    def per_cmd(self, cmd_one):
        contained = cmd_one.find("=")
        self.get_field(cmd_one, [True, cmd_one[contained+1:] if contained != -1 else ""])

    def parse(self):
        for cmd_one in self.cmds:
            if self.check(cmd_one):
                self.per_cmd(cmd_one)

    def do_server(self):
        if self.context.do_server[CMD] == cmd_opt_start_server:
            if not self.context.opt_port[ARG]:
                print("for start server, --port is required")
                return
            self.serv_sock = Server(int(self.context.opt_port[CMD]), "localhost")
            self.serv_sock.create()
            self.serv_sock.init_acceptor()
            print("server started")

        elif self.context.do_server[CMD] == cmd_opt_close_server:
            serv_sock.close()
            print("server closed")

    def do_message_impl(self, msg):
        i = 0
        while i < len(self.serv_sock.clients):
            self.serv_sock.send_msg(msg, i)
            i += 1

    def do_message(self):
        self.do_message_impl(self.context.do_message[CMD])

    def do_message_dump(self):
        self.do_message_impl("123")

    def do_help(self):
        print("%s=<start|close>, %s=<num_port>, %s, %s=<your text>, %s, %s" % (
        cmd_server, cmd_port, cmd_exit, cmd_msg, cmd_wait_conn, cmd_help))

    def do_delay(self):
        if self.context.do_timeout[ARG] and float(self.context.do_delay[THR]) >= float(self.context.do_timeout[CMD]):
            self.context.do_repeat[ARG] = False
            return
        delay = float(self.context.do_delay[CMD])
        sleep(delay)
        self.context.do_delay[THR] += delay

    def do_impl(self):
        if self.context.do_server[ARG]:
            self.do_server()
        if self.context.do_message[ARG]:
            self.do_message()
        if self.context.do_message_dump[ARG]:
            self.do_message_dump()
        if self.context.do_help[ARG]:
            self.do_help()
        if self.context.do_delay[ARG]:
            self.do_delay()

    def do(self):
        while True:
            self.do_impl()
            if not self.context.do_repeat[ARG]:
                break


def need_arg(cmd_one):
    for i in data_init:
        if i[0] == cmd_one:
            return i[1]


alias_container = list()





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
    dispersion = 0.0

    if len(cmd_list) > 0 and cmd_list[0] == cmd_repeat:
        serv_sock.schedule_task(cmd_line[len(cmd_repeat)+1:], 0)
        return

    for cmd_one in cmd_list:
        # exit
        if cmd_one == "--exit":
            return True
        # send auto-generated msg
        elif cmd_one == cmd_msg_dump:
            is_send_msg = True
            msg = serv_sock.dump_data
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
        # timeout
        elif is_cmd(cmd_one, cmd_tm)[0]:
            dis_ran = (float(random.random()) - 0.5) * dispersion
            sleep(float(is_cmd(cmd_one, cmd_tm)[1]) + dis_ran)
        elif is_cmd(cmd_one, сmd_dispersion)[0]:
            dispersion = float(is_cmd(cmd_one, сmd_dispersion)[1])
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
            serv_sock.init_acceptor()
            print("server started")

        elif server_opt == cmd_opt_close_server:
            serv_sock.close()
            print("server closed")

        else:
            print("invalid option for --server %s" % server_opt)

    if is_send_msg:
        iter = 0
        while iter < len(serv_sock.clients):
            serv_sock.send_msg(msg, iter)
            iter += 1

    if is_wait_conn:
        serv_sock.listen(1)
        serv_sock.wait_connection()
    # ---------------- end -----------------

    return False


def main():
    global serv_sock
    while True:
        sleep(0.3)
        cmd_line = input("please type command: ")
        if cmd_line == cmd_alias_server_start[0]:
            cmd_line = cmd_alias_server_start[1]

        cmd_worker = DoCmd(cmd_line, serv_sock)
        cmd_worker.do()

        # save server for next ops
        serv_sock = cmd_worker.serv_sock

        #is_exit = do_cmd(cmd_line)
        #if is_exit:
        #    break


main()
