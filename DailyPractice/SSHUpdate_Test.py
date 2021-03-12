#coding:utf-8
# by 20200415
"""
规则说明：
1、所有命令使用nohup，如
 nohup /usr/local/tomcat/tomcat7.0_jdk1.7_8086/AutoUpdate/updateShell.sh >/usr/local/tomcat/tomcat7.0_jdk1.7_8086/AutoUpdate/updateShell.log 2>&1
 2、存放的日志注明命名，多个的情况下要区分
"""
import ssh
import re
import time

#----------------------变量定义start-----------------------
linux_ip="192.168.8.32"
linux_port=22
linux_username="root"
linux_pwd="zjport"
#----------------------变量定义end-------------------------


class SSHCon:
	myclient=None
	chan=None
	def __init__(self,linux_ip,linux_port,linux_username,linux_pwd):
		# 新建一个ssh客户端对象
		self.myclient = ssh.SSHClient()
		# 设置成默认自动接受密钥
		self.myclient.set_missing_host_key_policy(ssh.AutoAddPolicy())
		# 连接远程主机
		self.myclient.connect(linux_ip, port=linux_port, username=linux_username, password=linux_pwd)
		self.chan=self.myclient.invoke_shell()#新函数
		return None	
	def cmd(self,cmd):
		print cmd	
		self.chan.send(cmd)		
		time.sleep(1)
	def close(self):
		self.myclient.close()	


def deployTheApp(path,app,url):
    mycon=SSHCon(linux_ip,linux_port,linux_username,linux_pwd)

    #----------------------1、停止应用-------------------------
    mycon.cmd(path+app+" 1000 \n")
    # ----------------------2、删除包-------------------------
    mycon.cmd("rm -rf "+path+"lib* \n")
    #----------------------3、拷贝Jenkins服务器上的包到tomcat目录下-------------------------
    mycon.cmd("wget --directory-prefix="+path+" "+url+" \n")
    time.sleep(10)
    #----------------------5、解压lib包-------------------------
    mycon.cmd("unzip -o "+path+"lib.zip -d "+path+" \n")
    time.sleep(10)
    #----------------------6、删除压缩包-------------------------
    mycon.cmd("rm -rf "+path+"lib.zip \n")
    time.sleep(10)
    #----------------------7、重新启动应用-------------------------
    mycon.cmd(path+app+" 0100 \n")
    #退出登录
    mycon.close()

if __name__ == "__main__":
    path = '/usr/local/tomcat/jar_TSN-10081-exchange-application/deploy/tsn-exchange-application/'
    app = 'tsn-exchange-application.sh'
    #url = 'http://192.168.3.239:8081/job/%E5%B7%A5%E7%A8%8B%20TSN-V1.0%EF%BC%88%E4%B8%96%E6%99%A8exchange-%E8%B4%BE%E6%B5%B7%E6%98%8E%EF%BC%89/ws/tsn-exchange-application/target/tsn-exchange-application/lib/*zip*/lib.zip'
    #url = 'http://192.168.3.239:8081/view/%E8%B4%BE%E6%B5%B7%E6%98%8E/job/TSN-V1.0\(%E4%B8%96%E6%99%A8exchange-%E8%B4%BE%E6%B5%B7%E6%98%8E\)/ws/tsn-exchange-parent-with-dependencies/tsn-exchange-application/target/tsn-exchange-application/lib/*zip*/lib.zip'

    url = 'http://192.168.3.239:8081/view/%E8%B4%BE%E6%B5%B7%E6%98%8E/job/tsn_exchange_git%EF%BC%88%E6%95%B0%E6%8D%AE%E4%BA%A4%E6%8D%A2-%E8%B4%BE%E6%B5%B7%E6%98%8E%EF%BC%89/ws/tsn-exchange-application/target/tsn-exchange-application/lib/*zip*/lib.zip'
    deployTheApp(path,app,url)
	
#上传整个文件夹
#os.system("scp -r /root/.jenkins/workspace/KWL-V1.0_task-execution\(执行定时任务-朱铁君\)/kwl-multiproject/kwl-task-execution/target/kwl-task-execution/lib root@192.168.3.138:/usr/local/etc/exchange/kwl-task-execution/deploy/kwl-task-execution/lib")

	

