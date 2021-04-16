import paramiko
import time
import configparser 
import os
import socket
import subprocess
client = paramiko.SSHClient()
cf = configparser.ConfigParser()
cf.read("config.ini")
ConfigIP = (cf.items("ServerConf"))
VsatIP = (cf.items("VsatPort"))

#定义查看端口是否正常
def PortSt(index=22):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(((ConfigIP[0][1]), index))
    if result == 0:
        print("Port %d is open" % index)
    else:
        print("Port %d is not open" % index)
    return(result)
# PortSt(3389)

#读取配置文件，定义IP地址
cf = configparser.ConfigParser()
cf.read("config.ini")
ConfigIP = (cf.items("ServerConf"))
VsatIP = (cf.items("VsatPort"))
#print(ConfigIP[1][1])
config = cf.sections()

#重启命令以及重启之前需要执行的命令，比如数据库提前关闭可以加快重启速度
Command = ['systemctl stop mysql','systemctl stop mongo','reboot']
#Command = ['ls','pwd','df -h','reboot']

#连接服务之前需要先判断小主机和服务器网络是否连同
def Ping( IP, Num=2):
   flag = (os.system(f"ping -n {Num} -w 2 {IP[0][1]}") )
#   stdin, stdout, stderr = (os.system(f"ping -c 1 -n {Num} -w 2 {IP[0][1]}"))
#  flag = (f"ping -c 1 -n {Num} -w 2 {IP[0][1]}")
#   print (stdout.read().decode('utf-8'))
#   print (stderr.read().decode('utf-8'))
   return(flag)

# Ping(ConfigIP)

# NUM = "10.10.10.1"
# PINGN = "ping -n 2"
# def Ping():
#    Number = 1
#    child = subprocess.Popen((PINGN)+" "+(ConfigIP[0][1]),shell=True,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
#    if (os.system(str(child))) == "0":
#       print ("aCCESS")
#       Number = 0
#    else:
#       print ("ERRORs")
#       Number = 2
#    child.wait()
#    print (Number)
#    return()
# print (ConfigIP[0][1])
# if Ping() == 0:
#    print ("access")


#定义连接服务器ssh
def ConnSv():
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   client.connect ( hostname = (ConfigIP[0][1]), port = (ConfigIP[1][1]),username = (ConfigIP[2][1]),password= (ConfigIP[3][1]) )
#   stdin, stdout, stderr = client.exec_command(Command[0])  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
#   print(flag)
   return
#Ping( ConfigIP,Num = 2)


def RestartServer():
   a = 0
   if Ping(ConfigIP)  == 0 and PortSt(22) == 0:
      ConnSv()
      for i in Command:
         #stdin, stdout, stderr = client.exec_command( (i) )  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值   
         client.exec_command( (i) )  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值   
         if i.strip() != "reboot":
            print ( (i),"执行成功" )
         elif i.strip() == "reboot":
            print ("服务器正在重启.....")
            time.sleep( 20 )
            if Ping(ConfigIP)  == 1:
               while a <= 10:
                  a += 1
                  if Ping(ConfigIP)  == 1 and  a < 10:
                     print ("重启中......",a)
                     time.sleep( 5 )
                  elif Ping(ConfigIP)  == 0:
                     a = 11
                     time.sleep (5)
                     print ("服务器重启完成",a)
                  elif Ping(ConfigIP)  == 1 and  a >= 10:
                     time.sleep (5)
                     print ("服务器重启失败,请联系SOMS维保经理高松",a)                  
                  else:
                     print("不满足条件",a)
            # elif Ping(ConfigIP,Num=2) == 0:
            #    print ("服务器重启完成")
   else:
      Ping(ConfigIP)  == 1 or PortSt(22) != 0
      print ("小主机到服务器网络断开，无法重启服务器，请检查驾驶室到集控室的网线")
      # 关闭SSHClient
   client.close()
   return

# RestartServer()