import os
import configparser
import paramiko
from Sreboot import PortSt
from Sreboot import Ping
#测试局域网和广域网连通性
cf = configparser.ConfigParser()
cf.read("config.ini")
ConfigIP = (cf.items("ServerConf"))
VsatIP = (cf.items("VsatPort"))
#print (VsatIP)
NUM = "-c 1 | grep 64 | cut -d \" \" -f 1 "
PING = "ping"
def NetST():
   if Ping(ConfigIP)  == 0 and PortSt(22) == 0:
      for x,y in VsatIP:
         client = paramiko.SSHClient()
         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         client.connect ( hostname = (ConfigIP[0][1]), port = (ConfigIP[1][1]),username = (ConfigIP[2][1]),password= (ConfigIP[3][1]) )
         # print (client.exec_command ( (PING)+" "+(y)+" "+(NUM)))# stdout 为正确输出，stderr为错误输出，同时是有1个变量有值ds
         stdin, stdout, stderr = client.exec_command ( (PING)+" "+(y)+" "+(NUM))# stdout 为正确输出，stderr为错误输出，同时是有1个变量有值ds
         #print (stdout.read().decode('utf-8'))
         # print (stderr.read().decode('utf-8'))
         #print (type(Status))
         #print (type(stderr.read().decode('utf-8')))
         if str(stdout.read().strip().decode()) == "64":
            print ( "服务器外网到", (x) ,(y), "网络正常" )
         else:
            print ( "服务器外网到", x ,(y), "网络异常" )
         client.close()
   else:
      Ping(ConfigIP)  == 1 or PortSt(22) != 0
      print ("小主机到服务器网络异常，无法测试，请检查驾驶室到集控室网络，或联系SOMS维保经理 高松")
   print ("网络测试完成，如有必要请再次测试，请拍照发给SOMS售后经理高松进行故障分析")
   return
#NetST()