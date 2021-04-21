#coding=utf8
'''
Created on 2018��5��16��

@author: yujia09962
'''
import random,os,time,re,datetime
from lib.util.TransitUtil import TransitUtil as TransitUtil
import lib.util.DbUtil as DbUtil
from lib.sys.Common import flag
from lib.sys.CheckFile import CheckFile

ACTIONPASS="PASS"
versionId = 0


class CollectUtilError(Exception):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


'''
createRandomChinese：创建指定长度随机中文的字符串
stringLen：随机字符串长度,默认长度为3
'''
def createRandomChinese(chineseLen:int=3):
    cerialString=""
    tmp=int(chineseLen)
    while tmp:
        cerialString+=chr(random.randint(19968,40869))
        tmp-=1
    return cerialString

'''
createRandomString：创建指定长度随机数字和字母的字符串
stringLen：随机字符串长度,默认长度为10
'''
def createRandomString(stringLen:int=10):
    cerialString=""
    tmp=int(stringLen)
    while tmp:
        tmpInt=random.randrange(1,63)
        if tmpInt<11:
            tmpInt+=47
        elif tmpInt<37:
            tmpInt+=54
        else:
            tmpInt+=60
        cerialString+=chr(tmpInt)
        tmp-=1
    return cerialString

def createRandomNum(stringLen:int=10):
    cerialString=""
    tmp=int(stringLen)
    while tmp:
        tmpInt=random.randrange(0,9)
        cerialString+=str(tmpInt)
        tmp-=1
    return cerialString

def createSerial(numbercount:int=0):
    from datetime import datetime
    Serial=str(datetime.now().strftime('%Y%m%d%H%M%S%f'))
    numbercount=int(numbercount)
    if numbercount==0:
        return Serial
    else:
        if numbercount>0 and numbercount<21:
            Serial=Serial[-numbercount:]
            return Serial
        elif numbercount>20:
            numelsecout=numbercount-20
            numelse=str(random.randint(int('1'+'0'*(numelsecout-1)), int('9'*numelsecout)))
            return numelse+Serial
        else:
            print('createSerial的参数值必须大于0，请检查！')
            raise CollectUtilError('createSerial的参数值必须大于0，请检查！')

def getName():
    """
    getName:随机生成姓名
    """
    import random as r
    surname = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
            '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
            '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
            '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
            '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
            '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
            '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '欧阳', '太史', '端木', '上官', '司马', '东方', '独孤', '南宫', '万俟', '闻人',
            '夏侯', '诸葛', '尉迟', '公羊', '赫连', '澹台', '皇甫', '宗政', '濮阳', '公冶', '太叔', '申屠', '公孙', '慕容', '仲孙', '钟离', 
            '长孙', '宇文', '司徒', '鲜于', '司空', '闾丘', '子车', '亓官', '司寇', '巫马', '公西', '颛孙', '壤驷', '公良', '漆雕', '乐正']

    namenum=r.choice([1,2]) 
    if namenum == 1:
        #name=r.choice(surname)+chr(r.randint(19968,40896))
        name=r.choice(surname)+chr(r.randint(19968,21000))
    else :
        #name=r.choice(surname)+chr(r.randint(19968,40896))+chr(r.randint(19968,40896))
        name=r.choice(surname)+chr(r.randint(19968,21000))+chr(r.randint(19968,21000))
    return name

def getMoble():
    """
    getMoble:随机生成手机号码
    """
    prefixArray = ("130", "131", "132", "133", "135", "137", "138", "170", "187", "189")
    i = random.randint(0, len(prefixArray)-1)
    prefix = prefixArray[i]
    telnum=createSerial(8)
    return prefix+telnum

def getTime(delayhour:int=0):
    """
    getTime:获取当前的时间+delayhour小时
    """
    import datetime
    nextTime = (datetime.datetime.now()+datetime.timedelta(hours=delayhour)).strftime('%Y-%m-%d %H:%M:%S')
    return nextTime

def getDay(delayday:int=1):
    """
    getDay:获取当前的时间+delayday天
        默认取下一天
    """
    import datetime
    NextDay = (datetime.datetime.now()+datetime.timedelta(days=delayday)).strftime('%Y-%m-%d %H:%M:%S')
    return NextDay 

def getEscapeDay(delayday:int=1):
    """
    getEscapeDay:获取当前的时间+delayday天,其中冒号进行转义
        默认取下一天
    """
    import datetime
    NextDay = (datetime.datetime.now()+datetime.timedelta(days=delayday)).strftime('%Y-%m-%d %H\:%M\:%S')
    return NextDay	

def getYearMonthDay(delayday:int=1):
    """
    getYearMonthDay:获取当前日期+delayday天，不带时分秒
        默认取下一天
    """
    import datetime
    NextDay = (datetime.datetime.now()+datetime.timedelta(days=delayday)).strftime('%Y-%m-%d')
    return NextDay 

def getYearMonthDay2(delayday:int=1):
    """
    getYearMonthDay2:获取当前日期+delayday天，不带时分秒，不带-
        默认取下一天
    """
    import datetime
    NextDay = (datetime.datetime.now()+datetime.timedelta(days=delayday)).strftime('%Y%m%d')
    return NextDay

def getId_no():
    """
    getId_no:随机生成身份证号
    """
    str1_6=["110101","150422","120101","130101","330101","440101","440113","441201",
            "340101","340201","450101","150101","150401","150423","150602","150801",
            "152501","152921"]
    str7_9=["195","196","197","198"]
    coefficientArray = [ "7","9","10","5","8","4","2","1","6","3","7","9","10","5","8","4","2"]# 加权因子
    MapArray=["1","0","X","9","8","7","6","5","4","3","2"]
    str10=str(random.randint(1, 9))
    str11_12 = str(random.randint(1, 12)).zfill(2)
    str13_14 = str(random.randint(1, 27)).zfill(2)
    str15_17 = str(random.randint(1, 999)).zfill(3)
    m = random.randint(0, len(str1_6)-1)
    n = random.randint(0, len(str7_9)-1)
    tempStr=str1_6[m]+str7_9[n]+str10+str11_12+str13_14+str15_17
    total = 0
    for i in range(len(tempStr)):
        total = total + int(tempStr[i])*int(coefficientArray[i])
    parityBit=MapArray[total%11]
    ResultIDCard=tempStr+parityBit
    return ResultIDCard

def getBank_account(fixed:str,cardnumlen:int,flag:int=0):
    """
    getBank_account:随机生成银行卡号，fixed:卡定，cardnumlen:卡号长度，flag:后缀是否是10标记（'0':否'1':是）
    """
    fixed_value=str(fixed)
    midlen = int(cardnumlen) - len(fixed_value)
    if fixed_value.isdigit() and str(cardnumlen).isdigit() and str(flag).isdigit():
        if int(flag):
            cardnum = fixed_value + createSerial(midlen - 2) + '10'
        else:
            cardnum = fixed_value + createSerial(midlen)
    else:
        print("银行卡预先设置信息都是数值格式，请检查！")
        cardnum = '0000000000000000'
    return cardnum

def _get_sftp(hostname, port, username, password):
    """
    _get_sftp：创建sftp连接
    """
    import paramiko
    try:
        t = paramiko.Transport((hostname, int(port)))  
        t.connect(username=username, password=password)  
        sftp = paramiko.SFTPClient.from_transport(t)
    except Exception as e:
        raise CollectUtilError('创建sftp连接出错，错误信息为：{0}，请确认！'.format(e)) 
    return sftp,t 
  
def _get_client(hostname, port, username, password):
    """
    _get_client：创建SSH连接
    """
    import paramiko
    try:
        client = paramiko.SSHClient()  
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        client.connect(hostname=hostname, port=int(port), username=username, password=password,timeout=5)
        paramiko.ssh_exception.AuthenticationException
    except Exception as e:
        raise CollectUtilError('创建ssh连接出错，错误信息为：{0}，请确认！'.format(e)) 
    return client  

def _getServerInfo(connect:str):
    connectList=connect.split(sep="@", maxsplit=1)
    ipPort=connectList[0]
    userPwd=connectList[1]
    ip=ipPort[:ipPort.find('@')]
    port=ipPort[ipPort.find('@')+1:]
    user=userPwd[:userPwd.find('/')]
    pw=userPwd[userPwd.find('/')+1:]
    
    return ip,port,user,pw

def _get_remote_server_info(sshcommand:str):
    #初始化数据变量
    
    SysConfigDict=TransitUtil.getSysConfig('sys_serverConfig')
    if SysConfigDict:
        connect=SysConfigDict.get('connect')
        ipaddr,port,username,passwd=_getServerInfo(connect)
    else:
        ipaddr,port,username,passwd=None,None,None,None
    #判断命令行中是否包含u或者p
    if r'ip' in sshcommand:
        ipaddr=re.findall(r'ip ([^|]+)', sshcommand)[0]
        sshcommand=sshcommand.replace(r'ip '+ipaddr,'')

    if r'port' in sshcommand:
        port=re.findall(r'port ([^|]+)', sshcommand)[0]
        sshcommand=sshcommand.replace(r'port '+port,'')

    if r'user' in sshcommand:
        username=re.findall(r'user ([^|]+)', sshcommand)[0]
        sshcommand=sshcommand.replace(r'user '+username,'')

    if r'pw' in sshcommand:
        passwd=re.findall(r'pw ([^|]+)', sshcommand)[0]
        sshcommand=sshcommand.replace(r'pw '+passwd,'')
        
    if ipaddr==None or port==None or username==None or passwd==None:
        raise CollectUtilError('服务器配置不正确，请ip、端口、用户名和密码信息是否正确')
    sshcommand=sshcommand.strip('|')
    return (sshcommand,ipaddr,port,username,passwd)

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

def execSshCommand(ip:str,port:int,user:str,pw:str,sshcommand:str,returnstr:str='pass_or_fail',ignore_error:bool = False):
    """
    execSshCommand：执行ssh命令,其中可包含ip、port、user、pw，分别对应服务器ip地址，端口、用户和密码：ip xx|port xx|user xx|pw xx
    sshcommand:需要执行的命令，使用|连接多条命令
    returnstr:返回的结果，如果是pass_or_fail则返回pass或者fail，如果为response,则返回服务器的返回信息
    """
    _available_backends()
    ipaddr,port,username,passwd=ip,port,user,pw
    #sshcommand,ipaddr,port,username,passwd=_get_remote_server_info(sshcommand)
    ssh = _get_client(ipaddr,port,username,passwd)
    commandlist = sshcommand.replace('|','\n')
    sttuple = ssh.exec_command(commandlist)
    stderr=sttuple[2]
    errstr=stderr.read()
    if errstr and ignore_error is False:
        ssh.close()
        message = '执行远程命令：'+commandlist+'出错信息：'+errstr.decode('utf8').strip('\n')
        print(message)
        raise CollectUtilError(message)
    if returnstr=='response':
        stdinfo=sttuple[1]
        infostr=stdinfo.read()
        return_info=infostr.decode('gbk').strip('\n')
    else:
        return_info=ACTIONPASS
    ssh.close()
    return return_info

def uploadFiles(remotepath:str,localpath:str,ipaddr:str,port:int,username:str,passwd:str,filename:str=''):
    """
    uploadFiles：上传文件
    """
    _available_backends()
    #初始化数据库变量
    sftp,t = _get_sftp(ipaddr,port,username,passwd)
    allfilepath=_getFilePathInFolder(localpath)
    if filename:
        for file in allfilepath:
            if re.match(filename+'$', os.path.basename(file)):
                sftp.put(file,remotepath+'/'+os.path.basename(file))
    else:
        for file in allfilepath:
            sftp.put(file,remotepath+'/'+os.path.basename(file))
    sftp.close()
    t.close()
    return ACTIONPASS

def downloadFiles(remotepath:str,localpath:str,ipaddr:str,port:int,username:str,passwd:str,filename:str=''):
    """
    uploadFiles：下载文件,返回下载后的文件本地路径列表
    """
    _available_backends()
    list_localfilepath=[]
    sftp,t = _get_sftp(ipaddr,port,username,passwd)
    files=sftp.listdir(remotepath)
    if filename:
        for file in files:
            if re.match(filename+'$', file):
                if not os.path.exists(localpath):
                    os.makedirs(localpath)
                sftp.get(remotepath+'/'+file,localpath+flag+file)
                list_localfilepath.append(localpath+flag+file)
    else:
        for file in files:
            sftp.get(remotepath+'/'+file,localpath+flag+file)
            list_localfilepath.append(localpath+flag+file)
    sftp.close()
    t.close()
    return list_localfilepath

def dbexecutefromfile(filename:str,filepath:str):
    """
    DbUtil.dbExecutefromfile:通过文件获取sql语句并执行,默认从testdata文件夹中获取文件
    """
    if os.path.isdir(filepath+filename):
        allfilepath=_getFilePathInFolder(filepath+filename)
    else: 
        allfilepath=[filepath+filename]
    for eachfile in allfilepath:
        if eachfile.lower().endswith(r'.sql'):
            need_run_sql='';
            for linestr in open(eachfile):
                if linestr:
                    need_run_sql +=linestr.replace('\n',' ')
                    if need_run_sql.strip().endswith(r';'):
                        DbUtil.dbExecute(need_run_sql.strip(),ignoreerror=True)
                        need_run_sql=''
    return ACTIONPASS

def get_remotesystem_date():
    return execSshCommand('date +%Y%m%d',returnstr='response')

def _getFilePathInFolder(path):
        ''''' 
        printPath:获取一个目录下的文件 
        '''
        # 所有文件  
        fileList = []  
        # 返回一个列表，其中包含在目录条目的名称
        if os.path.isdir(path):
            files = os.listdir(path)
            for f in files:
                filepath=path +'\\'+ f
                if(os.path.isfile(filepath)):  
                    # 添加文件  
                    fileList.append(filepath)
                else:
                    temp=_getFilePathInFolder(filepath+'\\')
                    fileList.extend(temp)
        else:
            fileList.append(path)
        return fileList

def wait(wait_time_or_sqlstr:str,sql_expected_str:str=None,timeOut:int=None):
    """
    wait：等待函数，等待指定的时间，或者执行SQL，直到等于期望的数值
    wait_time_or_sqlstr：为等待的时间，格式为数字，或者为SQL语句
    sql_expected_str：SQL语句的期望值，如果SQL查询出的结果和此期望值相同，则跳出循环，如果为-，则只要存在及跳出
    """
    from lib.support.DbOpe import SelectISNull
    curTime=0
    if not timeOut:timeOut=600
    if str(wait_time_or_sqlstr).isnumeric():
        wait_time_or_sqlstr=int(wait_time_or_sqlstr)
        while wait_time_or_sqlstr>0:
            time.sleep(1)
            wait_time_or_sqlstr-=1
    elif str(wait_time_or_sqlstr).lower().startswith('select'):
        if sql_expected_str is None:
            raise CollectUtilError("wait函数中请设置sql_expected_str期望结果字段")
        while True:
            try:
                if timeOut:
                    if curTime > int(timeOut):
                        return 'false'
                db_result = DbUtil.dbExecute(wait_time_or_sqlstr)[0]
                print("---------------------------------------")
                print("sql:" + str(wait_time_or_sqlstr))
                print("期望值:" + str(sql_expected_str))
                print("实际值:" + str(db_result))
                if str(db_result) == str(sql_expected_str) or str(sql_expected_str) == "-":
                    print("匹配成功，跳出wait循环")
                    break
                else:
                    time.sleep(1)
                    if timeOut:
                        curTime += 1
            except SelectISNull:
                print("查询结果为空，等待一秒")
                time.sleep(1)
                if timeOut:
                    curTime += 1
            except Exception as e:
                print("执行sql:{0}出现异常，异常信息为:{1}".format(wait_time_or_sqlstr, e))
                return 'false'
    return 'true'

def daysdiff(start_data:str,end_data:str):
    '''
    daysdiff:计算两个日志之间的日期总数
    start_data:格式为YYYYMMDD
    end_data:格式为YYYYMMDD
    return:返回天数
    '''
    import datetime
    start_data=start_data.replace('-','')
    start_data=start_data.replace('/','')
    end_data=end_data.replace('-','')
    end_data=end_data.replace('/','')
    start_data_datetime=datetime.datetime(int(start_data[:4]),int(start_data[4:6]),int(start_data[6:8]))
    end_data_datetime=datetime.datetime(int(end_data[:4]),int(end_data[4:6]),int(end_data[6:8]))
    return (end_data_datetime - start_data_datetime).days

def getUser_name():
    """
    getUser_name:随机商户用户名
    """
    telnum=createSerial(10)
    return "user"+telnum

def zkOperation(zkNode:str,zkData:str):
    #zk连接
    from kazoo.client import KazooClient
    gv_zkHost = TransitUtil.getVarByName("gv_zkHost")
    zk=KazooClient(hosts=gv_zkHost)
    zk.start()
    #zk数据写入
    zkresult=''
    if zk.exists(zkNode) != None:
        zkresult=zk.set(zkNode, zkData)
        print(zk.get(zkNode))
    else:
        zkresult=zk.create(zkNode, zkData)
    print(zkresult)
    return "pass"

def redisBakup():
    import redis
    #redisclient连接
    gv_redisIp = TransitUtil.getVarByName("$gv_redisIp")
    gv_redisSSHUser = TransitUtil.getVarByName("$gv_redisSSHUser")
    gv_redisSSHPwd = TransitUtil.getVarByName("$gv_redisSSHPwd")
    gv_redisPort = TransitUtil.getVarByName("$gv_redisPort")
    gv_redisPwd = TransitUtil.getVarByName("$gv_redisPwd")
    gv_redisFilePath = TransitUtil.getVarByName("$gv_redisFilePath")
    gv_redisFileName = TransitUtil.getVarByName("$gv_redisFileName")
    redis_pool = redis.ConnectionPool(host=gv_redisIp, port=gv_redisPort, password=gv_redisPwd, db=0)
    r = redis.Redis(connection_pool=redis_pool)
    #执行save备份
    r.bgsave()
    #将dump文件改名后放着
    ssh = _get_client(gv_redisIp,"22",gv_redisSSHUser,gv_redisSSHPwd)
    exCommand = 'mv '+gv_redisFilePath+'dump.rdb '+gv_redisFilePath+gv_redisFileName
    sttuple=ssh.exec_command(exCommand)
    stderr=sttuple[2]
    errstr=stderr.read()
    if errstr:
        ssh.close()
        message = '执行远程命令出错信息：'+errstr.decode('utf8').strip('\n')
        #message = '执行远程命令：'+commandlist+'出错信息：'+"".join(map(chr, list(errstr))).strip('\n')
        print(message)
        return 'fail'
    #cmd_result = stdout.read()
    #for line in cmd_result:
    #    print(line) 
    ssh.close()
    #清理redis内的内容
    r.flushdb()
    return 'pass'

def redisRecovery():
    from time import sleep
    gv_redisIp = TransitUtil.getVarByName("$gv_redisIp")
    gv_redisSSHUser = TransitUtil.getVarByName("$gv_redisSSHUser")
    gv_redisSSHPwd = TransitUtil.getVarByName("$gv_redisSSHPwd")
    gv_redisPort = TransitUtil.getVarByName("$gv_redisPort")
    gv_redisPwd = TransitUtil.getVarByName("$gv_redisPwd")
    gv_redisFilePath = TransitUtil.getVarByName("$gv_redisFilePath")
    gv_redisFileName = TransitUtil.getVarByName("$gv_redisFileName")
    gv_redisConfPath = TransitUtil.getVarByName("$gv_redisConfPath")
    ssh = _get_client(gv_redisIp,"22",gv_redisSSHUser,gv_redisSSHPwd)
    #将备份文件重命名回dump.rdb
    try:
        ssh = _get_client(gv_redisIp,"22",gv_redisSSHUser,gv_redisSSHPwd)
        exCommand = 'mv '+gv_redisFilePath+gv_redisFileName+' '+gv_redisFilePath+'dump.rdb'
        print(exCommand)
        ssh.exec_command(exCommand)
        stopCommand = gv_redisFilePath+'redis-cli -a '+gv_redisPwd+' -p '+gv_redisPort+' shutdown'
        startCommand = gv_redisFilePath+'redis-server '+gv_redisConfPath
        print(stopCommand)
        print(startCommand)
        ssh.exec_command(stopCommand)
        sleep(5)
        ssh.exec_command(startCommand)
    except Exception as e:
        print(e)
        return "fail"
    #打开redis端
    #运行重启命令
    return 'pass'

'''
createDateString：创建指定长度随机中文的字符串,默认获取当前时间，可针对天进行调整
days：根据当前天数进行调整的天数
'''
def createDateString(days:int=0,datestr:str=None):
    import datetime
    if datestr==None:
        datestr=datetime.datetime.now()
    else:
        datestr=datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
    datestr=datestr+datetime.timedelta(days=days)
    Serial=str(datestr.strftime('%Y-%m-%d %H:%M:%S'))
    return Serial

'''
createEffectiveTime：获得当前数据库中费用信息生效时间最长的数据,，针对天进行调整
days：根据当前天数进行调整的天数，默认为1天
'''
def createEffectiveTime(days:int=1):
    from lib.support.DbOpe import DBError
    from datetime import datetime
    #如果没有费用记录则使用当前时间作为第一条费用生效时间
    sshcommand = 'date "+%Y-%m-%d %H:%M:%S"'
    serverTime = execSshCommand(sshcommand,'response')
    gv_productDbName = TransitUtil.getVarByName("$gv_productDbName")
    sqlStr="select MAX(EFFECTIVE_TIME) from {0}.product_base_rates".format(gv_productDbName)
    try:
        dbSqlresult=DbUtil.dbExecute(sqlStr)[0]
        serverTimeObject=datetime.strptime(serverTime, '%Y-%m-%d %H:%M:%S')
        dbTimeObject=datetime.strptime(dbSqlresult, '%Y-%m-%d %H:%M:%S')
        sqlresult=serverTime if (serverTimeObject-dbTimeObject).days>0 else dbSqlresult
    except DBError:
        #如果没有费用记录则使用当前时间作为第一条费用生效时间
        sqlresult = serverTime
    Serial=createDateString(days=days,datestr=sqlresult)
    return Serial

def sqlDump():
    '''
    mysqldump方式进行数据库备份，从全局变量中获取参数，按照时间进行命名
    '''
    from datetime import datetime
    sqlDumpDir = TransitUtil.getVarByName("$gv_dbbakdir")
    if not os.path.exists(sqlDumpDir):
        os.mkdir(sqlDumpDir)
    gv_host = TransitUtil.getVarByName("$gv_host")
    gv_port = TransitUtil.getVarByName("$gv_port")
    gv_dbuser = TransitUtil.getVarByName("$gv_dbuser")
    gv_dbpasswd = TransitUtil.getVarByName("$gv_dbpasswd")
    dumpdate = datetime.now().strftime('%Y%m%d%H%M%S')
    #print(dumpdate)
    try:
        dumpCommand = 'mysqldump --host='+gv_host+' -P '+gv_port+' -u'+gv_dbuser+' -p'+gv_dbpasswd+' --skip-lock-tables --set-gtid-purged=off –hex-blob -f --all-databases> '+sqlDumpDir+'\DbDump_'+dumpdate+'.sql'
        #print(dumpCommand)
        os.system(dumpCommand)
    except Exception as e:
        print('{0}'.format(e))
    return 1

def sqlSource(filename:str=None):
    '''
    filename默认为none，如果传入了值就执行这个专门的文件
    '''
    sqlDumpDir = TransitUtil.getVarByName("$gv_dbbakdir")
    list_file = os.listdir(sqlDumpDir)
    list_file.sort(key=lambda fn:os.path.getmtime(sqlDumpDir+'\\'+fn))
    filepath = os.path.join(sqlDumpDir,list[-1])
    gv_host = TransitUtil.getVarByName("$gv_host")
    gv_port = TransitUtil.getVarByName("$gv_port")
    gv_dbuser = TransitUtil.getVarByName("$gv_dbuser")
    gv_dbpasswd = TransitUtil.getVarByName("$gv_dbpasswd")
    try:
        dumpCommand=('')
        if filename == None:
            dumpCommand = 'mysql --host='+gv_host+' -P '+gv_port+' -u'+gv_dbuser+' -p'+gv_dbpasswd+' --default-character-set=utf8 --binary-mode -f < '+filepath
        else:
            dumpCommand = 'mysql --host='+gv_host+' -P '+gv_port+' -u'+gv_dbuser+' -p'+gv_dbpasswd+' --default-character-set=utf8 --binary-mode -f < '+sqlDumpDir+'/'+filename
        #print(dumpCommand)       
        os.system(dumpCommand)        
    except Exception as e:
        print('{0}'.format(e))
    return 1

def getAccountByFile(cardbin:str=None):
    '''
    des: 随机生成银行卡
    parm: cardbin，默认为none，随机生成，传入具体carbin则生成对应的随机卡
    '''
    cardbinDict = {'622951': '16', '623151': '19', '621028': '16', '623039': '19', '622857': '19', '623121': '19', 
                   '622505': '18', '623518': '19', '621415': '19', '621625': '19', '622399': '17', '621287': '16', 
                   '622165': '16', '621817': '18', '427038': '16', '620403': '18', '623088': '19', '622363': '19', 
                   '622665': '16', '624301': '18', '621791': '16', '900003': '16', '694301': '18', '621905': '18', 
                   '622400': '17', '601382': '19', '623055': '16', '69580': '18', '621620': '19', '622510': '18', 
                   '620500': '16', '621734': '16', '622532': '19', '623020': '16', '621674': '19', '622310': '17', 
                   '623006': '18', '621721': '19', '433680': '16', '622953': '19', '468203': '16', '940047': '16', 
                   '622827': '19', '623123': '17', '602969': '16', '427571': '16', '622932': '16', '427028': '16', 
                   '603601': '17', '623190': '19', '622588': '16', '623539': '19', '621372': '19', '623251': '16', 
                   '623058': '19', '622396': '17', '621263': '18', '622324': '19', '621797': '19', '622379': '19', 
                   '621073': '19', '623136': '16', '621783': '19', '622806': '18', '623676': '19', '622986': '16', 
                   '621416': '16', '621735': '19', '622997': '19', '621460': '19', '622873': '19', '622303': '18', 
                   '621086': '19', '620082': '16', '622012': '18', '623022': '16', '621539': '19', '622152': '19', 
                   '622007': '18', '621377': '16', '623586': '19', '621511': '18', '622467': '19', '940072': '16', 
                   '622516': '16', '621496': '19', '621423': '16', '623070': '19', '621754': '19', '621090': '19', 
                   '621746': '17', '421393': '16', '627026': '19', '623001': '16', '62137320': '16', '623086': '16', 
                   '621562': '19', '621603': '18', '9896': '16', '621529': '19', '622879': '19', '622973': '19', 
                   '622425': '19', '621792': '16', '6858001': '19', '621413': '19', '622486': '16', '622402': '18', 
                   '622847': '19', '620905': '18', '622203': '19', '622132': '16', '968808': '16', '621600': '19', 
                   '620502': '18', '622188': '19', '621267': '18', '622291': '18', '622015': '18', '621010': '16', 
                   '620085': '16', '622848': '19', '62176410': '16', '621037': '19', '622129': '16', '621434': '16', 
                   '621910': '18', '620529': '19', '621327': '19', '601428': '17', '623803': '18', '415753': '16', 
                   '622876': '19', '622169': '19', '623002': '18', '621240': '19', '622375': '17', '940049': '18', 
                   '621391': '19', '622189': '19', '62176420': '16', '6223096510': '19', '434062': '16', '621462': '19', 
                   '623135': '19', '940046': '19', '622943': '19', '621804': '18', '622342': '19', '940063': '17', 
                   '622468': '18', '84380': '16', '622406': '17', '621371': '16', '95555': '16', '90592': '16', 
                   '622517': '16', '621760': '17', '622017': '18', '623182': '19', '623015': '18', '627068': '16', 
                   '622826': '19', '622967': '19', '621769': '16', '621050': '18', '622561': '19', '621578': '19', 
                   '622777': '16', '622684': '16', '623109': '19', '621765': '16', '955100': '19', '622978': '19', 
                   '622858': '19', '620062': '19', '940023': '16', '621750': '16', '622994': '16', '622865': '19', 
                   '621719': '19', '621633': '19', '623113': '19', '623644': '19', '620611': '18', '622821': '19', 
                   '623126': '16', '621673': '19', '622279': '18', '622002': '18', '622605': '18', '621666': '19', 
                   '622313': '18', '623569': '19', '624000': '18', '621525': '16', '623027': '19', '623063': '18', 
                   '621213': '19', '623658': '16', '621522': '18', '621029': '19', '621672': '19', '622700': '19', 
                   '623500': '18', '621305': '18', '621626': '19', '623040': '16', '622845': '19', '621662': '19', 
                   '940018': '16', '940008': '19', '60326500': '16', '622664': '16', '548259': '16', '940048': '19', 
                   '623272': '19', '621521': '16', '621074': '19', '623030': '19', '621616': '18', '621226': '19', 
                   '62218850': '19', '621912': '18', '623091': '19', '623179': '19', '621528': '16', '622340': '17', 
                   '622391': '16', '621661': '19', '442730': '16', '623185': '18', '621789': '19', '602907': '16', 
                   '623505': '16', '622673': '16', '621753': '19', '623172': '19', '622952': '16', '620107': '16', 
                   '622477': '19', '621590': '19', '621243': '18', '621376': '16', '621414': '19', '622418': '16', 
                   '620412': '18', '621807': '18', '621773': '16', '621497': '16', '621097': '19', '622945': '16', 
                   '940074': '18', '621585': '18', '627027': '19', '412963': '16', '621061': '19', '622828': '19', 
                   '622563': '19', '623171': '19', '621566': '19', '623120': '19', '622388': '16', '623669': '19', 
                   '621296': '19', '622395': '19', '622298': '16', '623062': '19', '622369': '16', '621374': '16', 
                   '621466': '16', '622970': '17', '621402': '18', '621751': '19', '623077': '19', '621453': '16', 
                   '622936': '19', '623037': '19', '623028': '19', '622958': '16', '622866': '16', '623253': '16', 
                   '622104': '18', '621485': '16', '622351': '16', '623328': '17', '622987': '18', '623309': '19', 
                   '622666': '16', '623036': '19', '623003': '19', '622018': '18', '623159': '16', '622154': '19', 
                   '87000': '16', '621517': '16', '621908': '18', '621091': '19', '621775': '19', '623000': '19', 
                   '621913': '18', '622946': '16', '621577': '19', '622338': '19', '623017': '16', '622366': '17', 
                   '622698': '16', '622960': '18', '622280': '19', '621239': '19', '622996': '19', '622667': '16', 
                   '623208': '19', '622928': '19', '621428': '16', '621690': '16', '621238': '19', '622138': '19', 
                   '623111': '16', '512425': '16', '622447': '16', '622660': '16', '623133': '19', '621068': '19', 
                   '9111': '19', '623128': '19', '621283': '19', '622903': '18', '622939': '17', '623038': '19', 
                   '621345': '18', '436742193': '19', '622404': '18', '622927': '19', '84342': '16', '622184': '19', 
                   '623116': '19', '966666': '18', '621084': '16', '622200': '19', '621731': '16', '621209': '18', 
                   '940016': '19', '622392': '19', '623200': '19', '621607': '18', '621370': '16', '62218849': '19', 
                   '621491': '16', '621558': '19', '623066': '19', '623260': '19', '621017': '19', '621042': '19', 
                   '622933': '19', '621748': '19', '622323': '19', '621488': '16', '623106': '17', '621021': '19', 
                   '621313': '18', '623042': '16', '621088': '19', '622153': '19', '621063': '16', '622337': '16', 
                   '622003': '18', '621738': '16', '621701': '19', '622982': '19', '621785': '19', '621095': '19', 
                   '623092': '16', '620061': '19', '622531': '19', '621208': '18', '623014': '18', '623602': '18', 
                   '95599': '19', '622615': '16', '620902': '18', '940017': '18', '623173': '19', '621759': '19', 
                   '621519': '19', '623573': '19', '623016': '16', '621761': '16', '621592': '16', '622929': '19', 
                   '622885': '16', '621325': '19', '622485': '18', '940002': '16', '621311': '18', '622111': '18', 
                   '60326513': '18', '62215051': '19', '6223092900': '19', '622128': '16', '621530': '19', '622281': '16', 
                   '621660': '19', '621351': '16', '623177': '19', '621798': '19', '622860': '16', '621361': '19', 
                   '621359': '18', '623041': '16', '621446': '19', '620712': '18', '622715': '18', '621598': '19', 
                   '622631': '16', '622443': '19', '622706': '18', '622135': '19', '621270': '18', '622133': '19', 
                   '623668': '19', '622355': '16', '622989': '16', '623011': '18', '622136': '18', '623321': '16', 
                   '623201': '19', '621568': '19', '621279': '16', '621285': '19', '622020': '18', '985262': '16', 
                   '621609': '18', '621406': '18', '623072': '19', '622662': '16', '620410': '18', '622886': '16', 
                   '621036': '19', '622297': '16', '622407': '19', '621448': '19', '620407': '18', '620088': '19', 
                   '622504': '18', '621724': '19', '623252': '19', '621561': '19', '622703': '18', '940053': '18', 
                   '621520': '19', '621252': '16', '622944': '16', '66405512': '17', '621531': '19', '622465': '17', 
                   '622137': '17', '621602': '18', '620060': '19', '87010': '16', '589970': '19', '621256': '19', 
                   '622208': '19', '623115': '16', '622259': '17', '620405': '18', '622470': '19', '622672': '16', 
                   '620904': '18', '621404': '18', '621212': '19', '433670': '16', '621459': '19', '621201': '16', 
                   '622411': '16', '622199': '19', '6223093370': '19', '622322': '16', '622972': '19', '621440': '17', 
                   '622881': '16', '622498': '19', '621303': '18', '621796': '16', '940013': '16', '621227': '19', 
                   '621300': '16', '623308': '19', '622278': '18', '621072': '19', '622668': '16', '621403': '19', 
                   '621360': '19', '621317': '18', '622937': '19', '621492': '16', '940040': '16', '620604': '18', 
                   '622367': '19', '622681': '19', '622893': '19', '621763': '19', '622403': '18', '622267': '18', 
                   '623125': '16', '621502': '18', '621211': '18', '402658': '16', '621733': '19', '622979': '19', 
                   '620302': '18', '940056': '17', '6223091100': '19', '621605': '18', '940027': '19', '9400301': '19', 
                   '620058': '19', '968807': '16', '621490': '16', '621070': '19', '623292': '16', '621289': '19', 
                   '623102': '16', '622302': '18', '622448': '16', '621105': '18', '621062': '16', '623560': '19', 
                   '622523': '16', '622439': '18', '622304': '18', '621599': '19', '621532': '19', '627028': '19', 
                   '621210': '18', '624100': '18', '621523': '16', '622368': '19', '621914': '18', '442729': '16', 
                   '622598': '16', '622110': '18', '623301': '18', '940060': '16', '410062': '16', '621362': '19', 
                   '472068': '16', '603708': '17', '623219': '19', '622261': '19', '622139': '16', '623068': '19', 
                   '620710': '18', '622691': '16', '623069': '19', '622140': '16', '622999': '19', '620612': '18', 
                   '622670': '16', '622609': '16', '622632': '16', '622410': '17', '623186': '16', '622331': '18', 
                   '940066': '19', '621331': '19', '621233': '19', '622955': '16', '621015': '19', '623094': '19', 
                   '621082': '16', '623178': '19', '623211': '19', '621005': '18', '621077': '16', '627069': '16', 
                   '621515': '19', '622114': '18', '622661': '16', '84385': '16', '623129': '19', '620522': '18', 
                   '940034': '17', '622846': '19', '621067': '19', '623189': '19', '96828': '16', '622844': '19', 
                   '436742': '19', '621476': '19', '621375': '19', '622181': '19', '621480': '19', '622384': '17', 
                   '622618': '16', '940021': '18', '622580': '16', '621103': '18', '621538': '19', '621033': '19', 
                   '62249802': '19', '621218': '19', '621099': '19', '621579': '19', '623075': '19', '623008': '18', 
                   '621225': '19', '622869': '19', '623698': '19', '622415': '16', '621292': '19', '621527': '19', 
                   '622870': '16', '620406': '18', '620607': '18', '621780': '19', '623263': '19', '622319': '16', 
                   '622824': '19', '621784': '19', '621772': '16', '621611': '18', '00601428': '17', '623229': '19', 
                   '622151': '19', '620402': '18', '622341': '16', '622959': '19', '690755': '18', '621237': '19', 
                   '984301': '16', '623155': '16', '622141': '16', '622280193': '19', '940015': '18', '621688': '19', 
                   '940037': '18', '622535': '16', '621281': '19', '622822': '19', '940025': '16', '622421': '19', 
                   '622427': '16', '621200': '19', '622867': '16', '622976': '19', '940003': '17', '622671': '16', 
                   '622690': '16', '620708': '18', '422161': '16', '623023': '16', '621065': '16', '999999': '16', 
                   '622993': '19', '622013': '18', '603445': '19', '621723': '19', '621290': '19', '940055': '17', 
                   '621464': '16', '621756': '19', '623076': '19', '623255': '16', '627025': '19', '623019': '19', 
                   '90010502': '16', '622562': '19', '621610': '18', '623099': '19', '621277': '16', '103': '19', 
                   '622180': '19', '62218851': '19', '622339': '16', '87030': '16', '621044': '19', '621221': '19', 
                   '620200': '18', '623098': '19', '623132': '19', '621614': '18', '621330': '19', '622258': '17', 
                   '621559': '19', '622855': '19', '621622': '19', '621066': '19', '620602': '18', '622260': '19', 
                   '621764': '16', '940073': '19', '526410': '16', '62215050': '19', '621273': '19', '623683': '16', 
                   '622682': '19', '62326536': '19', '621621': '19', '621340': '16', '402791': '16', '623100': '18', 
                   '623152': '19', '621302': '18', '623161': '19', '940029': '19', '624200': '18', '622487': '17', 
                   '620409': '18', '621080': '16', '620411': '18', '622343': '19', '621569': '19', '621205': '18', 
                   '621467': '19', '623258': '16', '621369': '19', '87050': '16', '620501': '19', '622316': '16', 
                   '622004': '18', '621060': '19', '623018': '19', '621337': '19', '621336': '19', '621915': '18', 
                   '621487': '16', '623901': '18', '623165': '18', '621288': '19', '623032': '19', '623521': '19', 
                   '940051': '16', '622422': '16', '940039': '19', '621782': '19', '621269': '16', '623218': '19', 
                   '621461': '19', '621008': '16', '623575': '19', '622949': '16', '998800': '16', '621217': '18', 
                   '622105': '18', '620518': '16', '621499': '16', '421317': '16', '95595': '19', '434061': '16', 
                   '84373': '16', '623271': '19', '622490': '17', '621096': '19', '622442': '19', '621613': '18', 
                   '621904': '18', '622511': '17', '621781': '16', '621725': '19', '6223093320': '19', '623021': '16', 
                   '624402': '18', '622301': '19', '621034': '16', '621665': '19', '621726': '19', '900000': '19', 
                   '623677': '19', '623287': '17', '622633': '16', '940076': '16', '621757': '19', '621526': '19', 
                   '622522': '16', '84301': '16', '524094': '16', '622312': '16', '623107': '19', '622005': '18', 
                   '552245': '16', '623656': '19', '622011': '18', '623516': '19', '623084': '19', '622904': '18', 
                   '620086': '19', '622692': '16', '622950': '16', '622506': '19', '621813': '18', '622127': '19', 
                   '621379': '19', '620706': '18', '623095': '19', '603367': '19', '622962': '17', '622538': '16', 
                   '621367': '16', '622172': '18', '623131': '19', '622877': '19', '620711': '18', '621309': '18', 
                   '622539': '16', '623007': '19', '415752': '16', '620535': '19', '623571': '19', '621463': '19', 
                   '622305': '18', '622882': '19', '422160': '16', '621216': '19', '621378': '16', '621405': '18', 
                   '622977': '19', '623010': '19', '622926': '19', '603694': '19', '621412': '18', '622998': '16', 
                   '621692': '16', '622849': '19', '6223093310': '19', '627067': '16', '621223': '19', '623199': '19', 
                   '95597': '19', '622963': '16', '621455': '19', '621743': '19', '622327': '17', '90020502': '16', 
                   '900105': '16', '621604': '18', '621452': '18', '415599': '16', '622345': '19', '623081': '16', 
                   '622167': '19', '622440': '16', '421349': '16', '95596': '19', '622518': '16', '621437': '19', 
                   '621333': '19', '940061': '16', '621228': '19', '940062': '19', '504923': '16', '622508': '16', 
                   '621619': '19', '621449': '19', '940070': '16', '621282': '19', '622990': '17', '621272': '16', 
                   '621081': '19', '940006': '17', '622362': '19', '622499': '19', '621722': '19', '623105': '16', 
                   '683970': '18', '940001': '19', '621348': '19', '621202': '18', '621696': '19', '621271': '19', 
                   '621749': '16', '621339': '19', '622019': '18', '622902': '18', '621207': '18', '622491': '17', 
                   '621235': '18', '438600': '16', '622938': '19', '621790': '19', '621004': '18', '623033': '19', 
                   '621016': '19', '621655': '19', '621617': '18', '623250': '16', '622630': '16', '622488': '16', 
                   '621057': '19', '940035': '18', '621601': '19', '621727': '19', '940050': '16', '622521': '16', 
                   '603602': '18', '620512': '18', '621606': '18', '623209': '18', '623065': '19', '621014': '16', 
                   '524011': '16', '621768': '16', '623108': '16', '622306': '18', '621560': '19', '621418': '19', 
                   '621468': '16', '433671': '16', '623012': '18', '623280': '16', '621732': '19', '620059': '19', 
                   '622147': '19', '95598': '19', '621788': '19', '622619': '16', '623170': '19', '623162': '19', 
                   '621741': '19', '623059': '18', '622150': '19', '621906': '18', '940057': '17', '622475': '16', 
                   '621469': '19', '622502': '18', '621280': '19', '623101': '19', '621026': '19', '623093': '19', 
                   '622674': '16', '621495': '16', '622455': '19', '622333': '16', '621489': '16', '62137310': '16', 
                   '622315': '18', '940032': '16', '623205': '19', '940044': '17', '622942': '16', '621670': '19', 
                   '621700': '19', '621903': '18', '623400': '18', '621222': '16', '622308': '18', '622492': '17', 
                   '621075': '19', '621793': '16', '66601428': '17', '621251': '19', '622016': '18', '621332': '19', 
                   '456351': '19', '621422': '19', '621745': '17', '623071': '19', '621083': '16', '621366': '19', 
                   '622947': '19', '621909': '18', '84361': '16', '622991': '18', '623510': '19', '622311': '17', 
                   '623096': '19', '623029': '16', '623035': '16', '622409': '19', '622271': '18', '622336': '17', 
                   '622412': '16', '621018': '19', '622365': '17', '623118': '19', '621663': '19', '623559': '16', 
                   '622332': '17', '623089': '19', '623310': '19', '623153': '19', '438588': '18', '621306': '18', 
                   '9558': '19', '622348': '16', '62364873': '19', '621206': '18', '621439': '19', '622823': '19', 
                   '62215049': '19', '622940': '19', '623168': '19', '621307': '18', '622513': '18', '621580': '19', 
                   '623700': '18', '622840': '19', '623056': '19', '621799': '19', '900205': '16', '621242': '19', 
                   '621291': '19', '622262': '19', '622696': '16', '94004604': '19', '621758': '19', '623158': '16', 
                   '622102': '18', '622859': '19', '94004602': '19', '622162': '19', '620714': '18', '622006': '18', 
                   '622622': '16', '621286': '16', '622509': '18', '622961': '16', '623203': '19', '623061': '18', 
                   '623523': '18', '621388': '19', '621728': '19', '622617': '16', '622202': '19', '412962': '16', 
                   '405512': '17', '621742': '19', '621411': '19', '622398': '16', '627066': '16', '940041': '17', 
                   '621814': '18', '620408': '18', '621457': '19', '303': '16', '62249804': '19', '621297': '19', 
                   '622988': '16', '622131': '19', '622892': '18', '622335': '16', '622620': '16', '623156': '16', 
                   '622010': '18', '622393': '16', '622568': '19', '621407': '18', '621582': '19', '621766': '19', 
                   '622604': '18', '621244': '16', '620704': '18', '621443': '19', '622394': '16', '621098': '19', 
                   '968809': '16', '621259': '16', '621911': '18', '622871': '16', '621767': '16', '940012': '16', 
                   '472067': '16', '621441': '19', '623181': '19', '622891': '19', '621433': '16', '621341': '16', 
                   '621298': '18', '621258': '16', '622272': '16', '621390': '16', '621589': '19', '621409': '18', 
                   '622935': '19', '621482': '19', '622292': '18', '623318': '19', '940069': '17', '621667': '19', 
                   '566666': '18', '622968': '19', '622317': '18', '621739': '19', '622930': '19', '621475': '19', 
                   '623083': '19', '621058': '19', '621465': '16', '623206': '19', '621284': '19', '940068': '17', 
                   '622856': '17', '621204': '18', '621268': '16', '623688': '19', '622983': '16', '621442': '17', 
                   '622536': '16', '622884': '16', '940031': '17', '888': '16', '940020': '16', '621102': '18', 
                   '621671': '19', '621245': '16', '940043': '17', '940038': '16', '87040': '16', '622382': '16', 
                   '622134': '16', '940054': '16', '623051': '19', '621778': '19', '623078': '19', '622864': '16', 
                   '621777': '16', '621304': '18', '427570': '16', '621786': '19', '621363': '19', '622173': '19', 
                   '940065': '19', '623050': '19', '621420': '16', '621498': '19', '621106': '18', '622980': '19', 
                   '621315': '18', '620527': '19', '622307': '18', '621536': '19', '90030': '16', '622359': '19', 
                   '621771': '16', '622663': '16', '621591': '16', '620609': '18', '940058': '16', '621035': '19', 
                   '621907': '18', '621107': '18', '623085': '19', '622992': '19', '621456': '17', '622325': '16', 
                   '623506': '19', '623196': '19', '623138': '19', '623262': '16', '940071': '19', '621755': '16', 
                   '621458': '19', '438589': '18', '623184': '19', '621019': '19', '623053': '19', '622616': '16', 
                   '621276': '16', '623013': '18', '622459': '17', '620503': '18', '621651': '19', '622489': '17', 
                   '623202': '18', '621691': '16', '621730': '16', '622328': '19', '623183': '18', '622478': '16', 
                   '622880': '16', '621669': '19', '623052': '19', '622931': '19', '623157': '16', '6223093330': '19', 
                   '622463': '19', '623087': '19', '6886592': '18', '990871': '18', '621977': '16', '622449': '16', 
                   '621041': '19', '62321601': '19', '621618': '19', '622146': '16', '622413': '16', '622126': '18', 
                   '623073': '16', '621266': '19', '622008': '18', '621636': '19', '623119': '19', '622441': '16', 
                   '623103': '19', '621720': '19', '623261': '19', '621408': '18', '621043': '19', '621752': '19', 
                   '621024': '16', '621076': '19', '621557': '19', '621901': '18', '621483': '16', '603506': '19', 
                   '621001': '18', '84390': '16', '621615': '18', '621352': '16', '623166': '18', '900010': '19', 
                   '421865': '16', '621089': '19', '622981': '18', '018572': '18', '621668': '19', '6223097910': '19', 
                   '620713': '18', '623034': '16', '623572': '19', '623026': '16', '622985': '18', '623699': '19', 
                   '621787': '19', '621588': '19', '621328': '19', '621518': '19', '620707': '18', '621770': '16', 
                   '621038': '19', '623079': '19', '622895': '16', '620516': '19', '622966': '16', '622314': '18', 
                   '622683': '19', '622309': '18', '00405512': '17', '621071': '19', '622843': '19', '622370': '19', 
                   '909810': '18', '940022': '16', '622275': '16', '622878': '18', '620802': '18', '620709': '18', 
                   '621795': '16', '84336': '16', '622644': '19', '940042': '18', '622897': '19', '622358': '19', 
                   '622841': '19', '622182': '19', '623048': '19', '622861': '16', '623188': '16', '621516': '19', 
                   '621203': '18', '623110': '16', '6091201': '18', '623259': '19', '622606': '18', '620528': '19', 
                   '62231902': '16', '623160': '19', '621744': '17', '622320': '16', '622908': '18', '984303': '16', 
                   '622862': '16', '622825': '19', '621030': '16', '623060': '19', '622429': '19', '622669': '16', 
                   '622329': '19', '622420': '17', '621747': '17', '623025': '19', '622170': '19', '621417': '19', 
                   '623090': '19', '622143': '19', '622971': '17', '622957': '16', '6223093380': '19', '621612': '18', 
                   '623686': '19', '621410': '18', '623269': '19', '621762': '19', '622452': '19', '623207': '19', 
                   '621486': '16', '621419': '19', '621013': '16', '6858009': '19', '623031': '19', '621533': '19', 
                   '621087': '19', '622909': '18', '622103': '18', '623067': '16', '990027': '18', '621608': '18', 
                   '622187': '19', '623139': '19', '620404': '18'}
    if cardbin is None:
        cardlist = list(cardbinDict.items())
        listlen = len(cardlist)
        num = random.randint(0,listlen)
        print(num)
        cardnum = cardlist[num][0]+createRandomNum(int(cardlist[num][1])-len(cardlist[num][0]))
    else:
        cardnum = cardbin + createRandomNum(int(cardbinDict[cardbin])-len(cardbin))
    return cardnum

def MD5Encrypt(md5str:str):
    '''
    MD5Encrypt：MD5加密字符串
    '''
    import hashlib
    md5str=str(md5str)
    m1 = hashlib.md5()
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token

def getTimeStamp(unit:str = 's', dateTime:str = None):
    '''
    getTimeStamp: 获取时间对应的时间戳，可以选择是
    dateTime: 默认空，获取当前执行机时间转化，传值则转化传入的时间的时间戳，支持格式"YYYY-MM-DD HH:mm:SS"
    unit: 可选则“s”或“ms”，默认“s”，分别对应秒时间戳和毫秒时间戳
    '''
    my_timestamp = None
    if dateTime is not None: 
        dateTime = time.mktime(time.strptime(dateTime, "%Y-%m-%d %H:%M:%S"))
    else:
        dateTime = time.time()
    if unit.lower() == 's':
        #print('s')
        my_timestamp = int(dateTime)
    elif unit.lower() == 'ms':
        #print('ms')
        my_timestamp = int(round(dateTime*1000))
    return my_timestamp


def executeSQL(sql:str):
    print("执行sql为："+sql)
    acutal = DbUtil.dbExecute(sql.strip())[0]
    print(acutal)
    return acutal


def test(waitTime:int,response:str="true"):
    time.sleep(waitTime)
    return response


def exeShellCommand(Command:str):
    """
    :param Command: 要执行的shell命令
    :return:
    """
    import os
    os.system(Command)

def getDateTimeStringByFormat(dateFormat:str='%Y%m%d%H%M%S'):
    """
    getDateTimeStringByFormat：创建指定格式的当前日期字符串，默认为20190828133700
    dateFormat：日期格式
    """
    import datetime
    return str(datetime.datetime.now().strftime(dateFormat))

def getDateTimeStringByFormatTest(date_string:str,now_date_format:str='%Y%m%d',target_date_format:str='%Y-%m-%d %H:%M:%S'):
    """
    getDateTimeStringByFormat：创建指定格式的当前日期字符串，默认为2019-08-28 13:37:00
    dateFormat：日期格式
    """
    import datetime
    return datetime.datetime.strptime(date_string, now_date_format).strftime(target_date_format)


def getDateString():
    """
    getDateString：创建20190828格式的的当前日期字符串
    """
    return getDateTimeStringByFormat('%Y%m%d')


def _modifyFileNameDate(fileName:str,dateString:str):
    fileNames = fileName.split("_")
    fileNames[4] = dateString
    return "_".join(fileNames)


def dealHbcbfBusinessConfirmFile(checkFile: CheckFile):
    # 重命名当前文件
    delimiter = checkFile.delimiter
    file_name = checkFile.file_name
    file_folder = checkFile.dest_file_store_path
    thirdpartApplyId = TransitUtil.getVarByName("thirdpartApplyId")
    gv_db_credit = TransitUtil.getVarByName("gv_db_credit")
    sql = "select loan_apply_id,apply_time,user_tel from "+gv_db_credit+".credit_loan_apply where thirdpart_apply_id='"+thirdpartApplyId+"'"
    loan_apply_id, apply_time, user_tel = DbUtil.dbExecute(sql, return_type="tuple")[0]
    apply_time = apply_time.strftime('%Y%m%d')
    with open(checkFile.file_path, encoding="utf-8") as tmpFile:
        targetName = _modifyFileNameDate(file_name, apply_time)
        destFilePath = os.path.join(file_folder, targetName)
        start_line, end_line = checkFile.get_data_lines()
        with open(destFilePath, mode="w+", encoding="utf-8") as destFile:
            # 处理文件数据
            for index, content in enumerate(tmpFile):
                if start_line <= index+1 <= end_line:
                    # 获取文件头字段
                    headers = content.split(delimiter)
                    # 获取头信息的随机数字字符串
                    headers[0] = thirdpartApplyId
                    headers[1] = apply_time
                    headers[2] = loan_apply_id
                    headers[6] = apply_time
                    headers[8] = user_tel
                    content = delimiter.join(headers)
                destFile.write(content)
            destFile.flush()
    # 删除当前文件信息
    os.remove(checkFile.file_path)
    # 将重新生成的文件设置成当前file_path
    checkFile.file_path = destFilePath


def uploadFilesForCheckFiles(destPath:str, ipaddr:str, port:int, username:str, passwd:str, checkFile:CheckFile):
    """
    uploadFilesForCheckFiles：上传校验文件
    destPath：sftp的目标目录
    ipaddr：sftp的ip
    port：sftp的端口
    username：sftp的连接用户名
    passwd：sftp的用户密码
    checkFile：需要上传的校验文件
    """
    _available_backends()
    # 初始化数据库变量
    sftp, t = _get_sftp(ipaddr, port, username, passwd)
    try:
        for file in checkFile.get_all_file_path():
            print("上传文件本地路径:"+file)
            if os.path.exists(file):
                print("目标路径:" + destPath + '/' + os.path.basename(file))
                sftp.put(file, destPath + '/' + os.path.basename(file))
            else:
                raise CollectUtilError("本地文件不存在，请确认")
    except Exception as e:
        raise e
    finally:
        sftp.close()
        t.close()
    return ACTIONPASS


def dealkoukuanjieguomingxiFile(checkFile: CheckFile):
    # 重命名当前文件
    delimiter = checkFile.delimiter
    file_name = checkFile.file_name
    file_folder = checkFile.dest_file_store_path

    tmp_file_name = "tmp_"+file_name
    tmp_file_Path = os.path.join(file_folder, tmp_file_name)
    checkFile.copy_file(tmp_file_name)

    thirdpartApplyId = TransitUtil.getVarByName("rpyOrdNo")
    gv_db_credit = TransitUtil.getVarByName("gv_db_credit")
    sql_no = "select certificate_no from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='"+thirdpartApplyId+"'"
    certificate_no, = DbUtil.dbExecute(sql_no, return_type="tuple")[0]
    sql = "select loan_apply_id, thirdpart_apply_id from " + gv_db_credit + ".credit_loan_apply where certificate_no = '"+certificate_no+"'"
    loan_apply_id, loan_thirdpart_apply_id = DbUtil.dbExecute(sql, return_type="tuple")[0]
    sql ="select repay_apply_id from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='"+thirdpartApplyId+"'"
    repay_apply_id, = DbUtil.dbExecute(sql, return_type="tuple")[0]
    sql = "select repay_amount,repay_term from " + gv_db_credit + ".credit_repay_order_detail where repay_apply_id='" + repay_apply_id + "'"
    repay_amount, repay_term = DbUtil.dbExecute(sql, return_type="tuple")[0]

    with open(tmp_file_Path, encoding="utf-8") as tmpFile:
        start_line, end_line = checkFile.get_data_lines()
        with open(checkFile.file_path, mode="w+", encoding="utf-8") as destFile:
            # 处理文件数据
            for index, content in enumerate(tmpFile):
                if start_line <= index+1 <= end_line:
                    # 获取文件头字段
                    headers = content.split(delimiter)
                    # 获取头信息的随机数字字符串
                    headers[0] = thirdpartApplyId
                    headers[2] = loan_thirdpart_apply_id
                    headers[6] = repay_term
                    headers[7] = repay_amount
                    headers[9] = loan_apply_id
                    content = delimiter.join(map(str, headers))
                destFile.write(content)
            destFile.flush()
    # 删除临时文件信息
    os.remove(tmp_file_Path)


def dealfenshengtiqianqingdaituihuoFile(checkFile: CheckFile):
    # 重命名当前文件
    delimiter = checkFile.delimiter
    file_name = checkFile.file_name
    file_folder = checkFile.dest_file_store_path

    tmp_file_name = "tmp_"+file_name
    tmp_file_Path = os.path.join(file_folder, tmp_file_name)
    checkFile.copy_file(tmp_file_name)

    thirdpartApplyId = TransitUtil.getVarByName("rpyOrdNo")
    gv_db_credit = TransitUtil.getVarByName("gv_db_credit")
    sql_no = "select certificate_no from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='"+thirdpartApplyId+"'"
    certificate_no, = DbUtil.dbExecute(sql_no, return_type="tuple")[0]
    sql = "select loan_apply_id, thirdpart_apply_id from " + gv_db_credit + ".credit_loan_apply where certificate_no = '"+certificate_no+"'"
    loan_apply_id, loan_thirdpart_apply_id = DbUtil.dbExecute(sql, return_type="tuple")[0]
    sql ="select repay_apply_id from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='"+thirdpartApplyId+"'"
    repay_apply_id, = DbUtil.dbExecute(sql, return_type="tuple")[0]
    sql = "select repay_amount from " + gv_db_credit + ".credit_repay_order_detail where repay_apply_id='" + repay_apply_id + "'"
    repay_amount, = DbUtil.dbExecute(sql, return_type="tuple")[0]

    with open(tmp_file_Path, encoding="utf-8") as tmpFile:
        start_line, end_line = checkFile.get_data_lines()
        with open(checkFile.file_path, mode="w+", encoding="utf-8") as destFile:
            # 处理文件数据
            for index, content in enumerate(tmpFile):
                if index == 0:
                    headers = content.split(delimiter)
                    headers[1] = repay_amount
                    content = delimiter.join(map(str, headers))
                elif start_line <= index+1 <= end_line:
                    # 获取文件头字段
                    headers = content.split(delimiter)
                    # 获取头信息的随机数字字符串
                    headers[0] = loan_thirdpart_apply_id
                    headers[2] = loan_apply_id
                    headers[6] = repay_amount
                    content = delimiter.join(map(str, headers))
                destFile.write(content)
            destFile.flush()
    # 删除临时文件信息
    os.remove(tmp_file_Path)


def dealfenshengtiqianqingdaituihuojiesuanFile(checkFile: CheckFile):
    # 重命名当前文件
    delimiter = checkFile.delimiter
    file_name = checkFile.file_name
    file_folder = checkFile.dest_file_store_path

    tmp_file_name = "tmp_"+file_name
    tmp_file_Path = os.path.join(file_folder, tmp_file_name)
    checkFile.copy_file(tmp_file_name)

    thirdpartApplyId = TransitUtil.getVarByName("rpyOrdNo")
    gv_db_credit = TransitUtil.getVarByName("gv_db_credit")
    sql_no = "select certificate_no from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='"+thirdpartApplyId+"'"
    certificate_no, = DbUtil.dbExecute(sql_no, return_type="tuple")[0]

    sql = "select thirdpart_apply_id from " + gv_db_credit + ".credit_loan_apply where certificate_no = '"+certificate_no+"'"
    loan_thirdpart_apply_id, = DbUtil.dbExecute(sql, return_type="tuple")[0]
    sql ="select repay_apply_id from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='"+thirdpartApplyId+"'"
    repay_apply_id, = DbUtil.dbExecute(sql, return_type="tuple")[0]
    sql = "select repay_amount from " + gv_db_credit + ".credit_repay_order_detail where repay_apply_id='" + repay_apply_id + "'"
    repay_amount, = DbUtil.dbExecute(sql, return_type="tuple")[0]

    with open(tmp_file_Path, encoding="utf-8") as tmpFile:
        start_line, end_line = checkFile.get_data_lines()
        with open(checkFile.file_path, mode="w+", encoding="utf-8") as destFile:
            # 处理文件数据
            for index, content in enumerate(tmpFile):
                if index == 0:
                    headers = content.split(delimiter)
                    headers[1] = repay_amount
                    content = delimiter.join(map(str, headers))
                elif start_line <= index+1 <= end_line:
                    # 获取文件头字段
                    headers = content.split(delimiter)
                    # 获取头信息的随机数字字符串
                    headers[0] = loan_thirdpart_apply_id
                    headers[4] = repay_amount
                    content = delimiter.join(map(str, headers))
                destFile.write(content)
            destFile.flush()
    # 删除临时文件信息
    os.remove(tmp_file_Path)


def downloadFilesToTestDataFolder(remotepath:str,ipaddr:str,port:int,username:str,passwd:str,filename:str=''):
    """
    downloadFilesToTestDataFolder：下载文件到临时运行目录
    """
    localpath = TransitUtil.getReportFolder()
    _available_backends()
    list_localfilepath=[]
    sftp,t = _get_sftp(ipaddr,port,username,passwd)
    files=sftp.listdir(remotepath)
    if filename:
        for file in files:
            if re.match(filename+'$', file):
                if not os.path.exists(localpath):
                    os.makedirs(localpath)
                sftp.get(remotepath+'/'+file,localpath+flag+file)
                list_localfilepath.append(localpath+flag+file)
    else:
        for file in files:
            sftp.get(remotepath+'/'+file,localpath+flag+file)
            list_localfilepath.append(localpath+flag+file)
    sftp.close()
    t.close()
    return list_localfilepath


def modify_settle_files(downloadPath:str,ipaddr:str,port:int,username:str,passwd:str):
    import shutil
    local_files = downloadFilesToTestDataFolder(downloadPath,ipaddr,port,username,passwd)
    tp = "{0}|{1}|S|SUCCESS|123|1254|100|\n"

    time_string = getDateString()

    need_up = []
    for o in local_files:
        file_name = os.path.basename(o)
        if "hebao" in file_name:
            tmp_file_name = "BACK_" + os.path.basename(o)
            tmp_file_path = os.path.join(os.path.dirname(o), tmp_file_name)
            # shutil.copy(o, tmp_file_path)
            with open(tmp_file_path, mode="w", encoding="utf-8") as tFile:
                for index, line in enumerate(open(o, encoding="utf-8")):
                    if index > 0 and not line.startswith("@"):
                        line = line.strip("\n") + tp.format(createRandomString(20),time_string)
                    elif index == 0:
                        line = line.strip("\n")+line.strip("\n")+"0|0|\n"
                    tFile.write(line)
            need_up.append(tmp_file_path)
    return str(need_up)


def upload_settle_files(remotepath:str, filePaths:str,ipaddr:str,port:int,username:str,passwd:str):
    """
    upload_settle_files：上传文件
    """
    _available_backends()
    #初始化数据库变量
    sftp,t = _get_sftp(ipaddr,port,username,passwd)
    allfilepath= eval(filePaths)
    sshcommand = "mkdir -p "+remotepath
    execSshCommand(ipaddr,port,username,passwd,sshcommand=sshcommand,ignore_error=True)
    for file in allfilepath:
        print(file)
        sftp.put(file,remotepath+'/'+os.path.basename(file))
    sftp.close()
    t.close()
    return ACTIONPASS


def check_repay_files(filePaths:str):
    """
    check_repay_files：校验文件
    """
    error_apply_id = []
    gv_db_credit = TransitUtil.getVarByName("gv_db_credit")
    filePaths = eval(filePaths)
    for file in filePaths:
        for index,line in enumerate(open(file,encoding="utf-8")):
            if index > 0 and not line.startswith("@"):
                lines = line.split("|")
                apply_id = lines[7]
                sql_1 = "select repay_status from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='{}'".format(apply_id)
                repay_status, = DbUtil.dbExecute(sql_1, return_type="tuple")[0]
                if str(repay_status) != "1":
                    error_apply_id.append(apply_id)
                    print(str(apply_id)+"的状态不正确，当前值为:"+str(repay_status))
    if error_apply_id:
        raise CollectUtilError("还款文件校验失败，以下申请id记录状态不为1：{}".format(error_apply_id))
    return apply_id


def check_repay_files_for_back(filePaths:str):
    """
    check_repay_files_for_back：批量扣款明细回盘文件差异比对
    """
    error_apply_id = []
    gv_db_credit = TransitUtil.getVarByName("gv_db_credit")
    filePaths = eval(filePaths)
    for file in filePaths:
        for index,line in enumerate(open(file,encoding="utf-8")):
            if index > 0 and not line.startswith("@"):
                lines = line.split("|")
                apply_id = lines[7]
                sql_1 = "select check_status from " + gv_db_credit + ".credit_check_file_info where our_order_no = (select repay_apply_id from " + gv_db_credit + ".credit_repay_order where thirdpart_apply_id='{}')".format(apply_id)
                repay_status, = DbUtil.dbExecute(sql_1, return_type="tuple")[0]
                if str(repay_status) != "CHECKED":
                    error_apply_id.append(apply_id)
                    print(str(apply_id)+"的值不正确，当前值为:"+str(repay_status))
    if error_apply_id:
        raise CollectUtilError("还款文件校验失败，以下申请id记录值不为CHECKED：{}".format(error_apply_id))
    return "true"


def change_server_time(ipaddr: str, port: int,username: str, passwd: str, scriptPath: str, modules: str, date_string: str, mode: str=""):
    """
    使用脚本更改服务器时间
    ipaddr：脚本存放的host
    port：连接host的端口
    username：连接host的用户
    passwd：连接host的用户密码
    scriptPath：脚本存放目录
    modules：需要更改时间的模块
    date_string：更改的时间字符串，格式为20100106
    """
    print("本次切时间的应用为" + modules)
    import datetime
    try:
        datetime.datetime.strptime(date_string, '%Y%m%d')
    except ValueError:
        raise CollectUtilError("时间格式不正确，请参考：20200106")
    command = "sh " + scriptPath + " " + modules + " " + date_string
    command = command + " " + mode if mode else command
    return execSshCommand(ipaddr, port, username, passwd, command)

def getTimeSting():
    return  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def createUserInfo():
    """
    :return: 返回用户基本信息，userName,wid,idcard,datetime
    """
    return getName(),createRandomNum(20),getId_no(),getTimeSting(),getMoble(),getAccountByFile()
	
def exeSql(sql_str):
    """
    :param sql_str: 需要执行的sql语句
    :return: 执行sql结果
    """
    print("执行sql为："+sql_str)
    try:
        db_result = DbUtil.dbExecute(sql_str)[0]
    except Exception as e:
        raise CollectUtilError('执行sql出错，错误信息为：{0}，请确认！'.format(e))
        print('{0}'.format(e))
        db_result = None
    return db_result

def getTimenow():
    return int(datetime.datetime.now().strftime('%Y%m%d'))
	
def excuteSQLAndCheck(sql:str,except_value:str):
    print("执行sql为："+sql)
    actual_value = exeSql(sql)
    if str(actual_value) == str(except_value):
        return "true"
    else:
        raise CollectUtilError("对比失败，期望值：{0},实际值：{1}".format(except_value,actual_value))