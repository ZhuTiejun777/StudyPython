# coding = UTF-8
import paramiko
import re
import argparse
import datetime
import threading
import os

from jvm.utils import print_message


class JVMError(Exception):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


def _available_backends():
    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]


def _get_client(hostname: str, port: int, username: str, password: str):
    """
        _get_client：创建SSH连接
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, port=int(port), username=username, password=password, timeout=5)
    except Exception as e:
        raise JVMError('创建ssh连接出错，错误信息为：{0}'.format(e))
    return client


def _exec_command(client, command: str):
    """
        _exec_command: 连接服务器发送命令
    """
    _available_backends()
    if client is None:
        raise JVMError('未初始化连接对象')
    try:
        stdin, stdout, stderr = client.exec_command("bash --login -c '{}'".format(command))
        err = stderr.read().decode('utf8').strip('\n')
        if err:
            raise JVMError(err)
        else:
            return stdout.read().decode('utf8').strip('\n')
    except Exception as e:
        raise JVMError('执行远程命令出错，错误信息为：{0}'.format(e))


def _async_exec_command(client, command: str):
    _available_backends()
    if client is None:
        raise JVMError('未初始化连接对象')
    try:
        stdin, stdout, stderr = client.exec_command("bash --login -c '{}'".format(command))
        line_buf = b''
        while not stdout.channel.exit_status_ready():
            line_buf += stdout.read(1)
            if line_buf.endswith(b'\n'):
                yield line_buf.decode('utf8').strip('\n')
                line_buf = b''
    except Exception as e:
        raise JVMError('执行远程命令出错，错误信息为：{0}'.format(e))


class JVMMonitor:
    jps_command = "jps -v"
    jps_command_export = "export TERM = xterm"
    source_command = "source ~/.bash_profile"
    thread_info_command = "top -H -b -n 1 -p {pid}"
    get_term_command = "echo $TERM"
    set_term_command = "export TERM={}"
    jstack_command = "jstack {pid}"
    jstat_command = "jstat -gc {pid} {sleep} {count}"
    jstat_util_command = "jstat -gcutil {pid} {sleep} {count}"

    men_argument_parser = None
    thread_argument_parser = None

    def __init__(self, hostname: str, port: int, username: str, password: str):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh_client = None
        self.pid = None
        self.pid_name = None
        # 存放进程信息
        self.pid_collector = {}
        self.pid_title = ["index", "pid", "java", "command"]
        # 采样的时间间隔
        self.sleep = 5
        self.is_term = False
        # 监控文件存放目录
        self.monitor_folder = os.path.join("result")
        # 命令头
        self.cmd = "{}@{}：".format(self.hostname, self.username)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        # 创建客户端连接
        if self.ssh_client is None:
            self.ssh_client = _get_client(self.hostname, self.port, self.username, self.password)
            # 加载环境变量
            _exec_command(self.ssh_client, self.source_command)

    def close(self):
        # 关闭客户端连接
        if self.ssh_client is not None:
            self.ssh_client.close()
            self.ssh_client = None

    def get_pid(self, can_more=False):
        # 获取远程java进程
        jps_infos = _exec_command(self.ssh_client, self.jps_command)
        # 获取所有的进程号
        if jps_infos:
            pid_collector = []
            for index, jps_info in enumerate(jps_infos.split("\n")):
                pid, java, command = jps_info.split(" ", 2)
                pid_collector.append([index, pid, java, command])
                _, self.pid_collector[pid] = java.rsplit("/", 1) if "/" in java else ("", java)
            print("远程JAVA进程列表如下：")
            print_message(pid_collector, self.pid_title)
            if can_more is False:
                pid = input("请输入需要监控的进程index，退出请输入E：")
            else:
                pid = input("请输入需要监控的进程index，多个以空格隔开，退出请输入E：")
            while True:
                if pid.lower() == "e":
                    return None
                else:
                    if can_more is False:
                        item_index = int(pid)
                        if item_index >= len(pid_collector):
                            pid = input("请输入正确的index，退出请输入E：")
                        else:
                            _, pp,  self.pid_name, _ = pid_collector[item_index]
                            return pp
                    else:
                        var2 = []
                        for var1 in re.split("\\s+", pid):
                            var1 = int(var1)
                            if var1 >= len(pid_collector):
                                continue
                            else:
                                _, pp, _, _ = pid_collector[var1]
                                var2.append(pp)
                        return var2
        else:
            print("没有可监控的JAVA进程")
            return None

    def _get_thread_pid_name(self):
        # 获取线程名
        all_thread_infos = self.get_thread_stack()
        thread_pid_name = {self.pid: self.pid_name}
        thread_pid_state = {self.pid: ""}
        # 根据线程号获取线程名
        for all_thread_info in all_thread_infos:
            find_pid = re.findall("nid=([0-9a-zA-Z]+)", all_thread_info)
            if find_pid:
                pid = str(int(find_pid[0], 16))
                thread_name = all_thread_info[:all_thread_info.index('"', 1)].strip('" ')
                thread_pid_name[pid] = thread_name
                thread_state = re.findall("java.lang.Thread.State: ([^\n]+)", all_thread_info)
                if thread_state:
                    thread_pid_state[pid] = thread_state[0]
                else:
                    thread_pid_state[pid] = ""
        return thread_pid_name, thread_pid_state

    def get_thread_info(self):
        if self.pid:
            command_column = None
            pid_column = None
            thread_pid_name, thread_pid_state = self._get_thread_pid_name()
            # 设置term
            if self.is_term is False:
                term = _exec_command(self.ssh_client, self.get_term_command)
                _exec_command(self.ssh_client, self.set_term_command.format(term))
                self.is_term = True
            thread_infos = _exec_command(self.ssh_client, self.thread_info_command.format(pid=self.pid))
            # 开始解析线程信息
            if thread_infos:
                thread_info_collector = []
                thread_title_collector = None
                is_starting = False
                for thread_info in thread_infos.split("\n"):
                    thread_info_column_value = re.split("\\s+", thread_info.strip())
                    if 'PID' in thread_info_column_value:
                        # 如果PID关键字在此列表中，说明列名行数开始
                        thread_title_collector = thread_info_column_value
                        # 获取命令和线程号
                        command_column = thread_info_column_value.index("COMMAND")
                        pid_column = thread_info_column_value.index("PID")
                        # 增加线程状态列
                        thread_title_collector.append("STATE")
                        is_starting = True
                        continue
                    if is_starting:
                        thread_info_column_value[command_column] = thread_pid_name.get(thread_info_column_value[pid_column])
                        thread_info_column_value.append(thread_pid_state.get(thread_info_column_value[pid_column]))
                        thread_info_collector.append(thread_info_column_value)
                print_message(thread_info_collector, thread_title_collector)
                return thread_info_collector

    def get_thread_stack(self, thread_pid=None):
        stack_infos = _exec_command(self.ssh_client, self.jstack_command.format(pid=self.pid))
        all_thread_infos = stack_infos.split("\n\n")
        if thread_pid:
            # 通过正则拿到起始行
            for thread_info in all_thread_infos:
                if "nid={}".format(thread_pid) in thread_info:
                    print(thread_info)
                    break
            else:
                print("没有找到执行线程信息")
        return all_thread_infos

    def get_men_info(self, pid, command, sleep: int = 1000, count: int = 1, dst_file=None):
        file = None
        if dst_file:
            file = open(dst_file, mode="w", encoding="UTF-8")
        for jstat_info in _async_exec_command(self.ssh_client, command.format(
                pid=pid,
                sleep=sleep,
                count=count)
                                              ):
            if file:
                file.write(jstat_info + "\n")
            else:
                print(jstat_info)
        if file:
            file.close()

    def _argument_parser(self):
        # 初始化传参配置
        self.men_argument_parser = argparse.ArgumentParser()
        self.men_argument_parser.add_argument("-c", type=int, help='统计的次数', default=1)
        self.men_argument_parser.add_argument("-s", type=int, help='等待的时间', default=1000)
        self.men_argument_parser.add_argument("-d", type=str, help='记录的文件名', default=None)

        self.thread_argument_parser = argparse.ArgumentParser()
        self.thread_argument_parser.add_argument("-t", type=int, help='线程pid', default=None)

        self.root_argument_parser = argparse.ArgumentParser()
        self.root_argument_parser.add_argument("thread", help='线程数据')
        self.root_argument_parser.add_argument("jps", help='JAVA进程列表')
        self.root_argument_parser.add_argument("men", help='JAVA内存状态')
        self.root_argument_parser.add_argument("menutil", help='JAVA内存百分比状态')
        self.root_argument_parser.add_argument("monitor", help='JAVA监控')
        self.root_argument_parser.add_argument("exit", help='退出监控')

    def monitor_men(self):
        # 初始化存放目录
        #rootFile = os.path.abspath(os.path.dirname(__file__))
        monitor_folder = os.path.join(self.monitor_folder, self.hostname, "men")
        if not os.path.exists(monitor_folder):
            os.makedirs(monitor_folder)
        monitor_active = input("是否只监控当前进程[y/n]：")
        if monitor_active.lower() == "n":
            pid = self.get_pid(can_more=True)
        else:
            pid = [self.pid]
        monitor_sleep = input("请输入监控间隔，默认1s：")
        monitor_sleep = int(monitor_sleep) if monitor_sleep else 1
        monitor_time = input("请输入监控时间[s]：")
        monitor_count = int(int(monitor_time) / monitor_sleep)
        run_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_collect = []
        for monitor_pid in pid:
            dst_file = os.path.join(monitor_folder, str(self.pid_collector[monitor_pid]) + "-" + run_time)
            file_collect.append(dst_file)
            threading.Thread(target=self.get_men_info, args=(
                monitor_pid, self.jstack_command, monitor_sleep * 1000, monitor_count, dst_file)).start()
        print("开始监控，监控结果：\n" + "\n".join(file_collect))

    def start(self, pid=None):
        self._argument_parser()

        pid = pid or self.get_pid()
        if pid:
            self.pid = pid
            while True:
                try:
                    print("-" * 90)
                    cmd = input(self.cmd)
                    cmd = cmd.strip()
                    cmd_and_args = re.split("\\s", cmd)
                    if cmd == "-h":
                        self.root_argument_parser.parse_args(cmd_and_args)
                    else:
                        if cmd_and_args[0] == "thread":
                            thread_args = self.thread_argument_parser.parse_args(cmd_and_args[1:])
                            if thread_args.t:
                                thread_pid = hex(thread_args.t)
                                self.get_thread_stack(thread_pid)
                            else:
                                # 如果不存在参数，则展示所有线程信息
                                self.get_thread_info()
                        elif cmd_and_args[0] == "jps":
                            pid = self.get_pid()
                            if pid:
                                self.pid = pid
                            else:
                                print("")
                        elif cmd_and_args[0] == "men":
                            men_args = self.men_argument_parser.parse_args(cmd_and_args[1:])
                            self.get_men_info(self.pid, self.jstat_command, men_args.s, men_args.c, men_args.d)
                        elif cmd_and_args[0] == "menutil":
                            men_args = self.men_argument_parser.parse_args(cmd_and_args[1:])
                            self.get_men_info(self.pid, self.jstat_util_command, men_args.s, men_args.c, men_args.d)
                        elif cmd_and_args[0] == "monitor":
                            self.monitor_men()
                        elif cmd_and_args[0].lower() == "exit" or cmd_and_args[0].lower() == "e":
                            break
                except SystemExit:
                    pass


if __name__ == "__main__":

    dst_id = "192.168.66.170"
    # dst_id = "10.253.77.58"
    dst_port = 22
    dst_user = "root"
    dst_pwd = "yrjk%!123098"

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", type=str, help='目标地址', default=None)
    argument_parser.add_argument("-p", type=int, help='目标端口', default=None)
    argument_parser.add_argument("-u", type=str, help='访问用户', default=None)
    argument_parser.add_argument("-w", type=str, help='访问密码', default=None)
    args = argument_parser.parse_args()

    ip = args.i or dst_id
    p = args.p or dst_port
    user = args.u or dst_user
    pwd = args.w or dst_pwd

    if ip and p and user and pwd:
        with JVMMonitor(ip, p, user, pwd) as jvm_monitor:
            jvm_monitor.start()
    else:
        print("参数数据不完整，请输入数据库连接信息，使用-h了解参数")
