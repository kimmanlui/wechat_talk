#!/usr/bin/python
# -*- coding: UTF-8 -*-
# The program is based on wxpy library. 
# Ref: https://github.com/youfou/wxpy
# FOR PYTHON 27 ON WINDOWS
# 用户自行设计关键字对话
# support : https://stackoverflow.com/questions/26473681/pip-install-numpy-throws-an-error-ascii-codec-cant-decode-byte-0xe2


d={"help"         : "谢谢你对UIC-ACE课程感兴趣，你可以打如下关键字 [1] course  [2] registration [3] discount" , 
   "test"         : "ACE chatbot is working fine. " ,
   "course"       : "目前有 [1] 危机管理  [2] SAT 等",
   "registration" : "使用手机或电脑打开uic.edu.hk/en/ace/application然后填下表格，便完成！",
   "discount"     : "some coure has early bird discount" ,
   "危机管理"      : "这是非常好的课程", 
   "SAT"          : "early-bird discount before 1 Nov 2017", 
   "1"            : "不要打数字，打小写英文或中文关键字"  ,
   "2"            : "不要打数字，打小写英文或中文关键字"  ,
   "3"            : "不要打数字，打小写英文或中文关键字"  ,
   "4"            : "不要打数字，打小写英文或中文关键字"  ,
   "*autoreply"   : "自动回复，这是微信客服机械人，请输入 help " } 


#Change the default encoding for Chinese characters
#http://blog.csdn.net/a657941877/article/details/9063883
from wxpy import *
import datetime
import codecs

import sys   
reload(sys)   
sys.setdefaultencoding('utf-8')   

logFile   ="winchatbot.log"
actionFile="wintalk.txt"

def get_curtime():
    curtime=datetime.datetime.now().strftime("%I:%M%p on %B %d,%Y")
    return(curtime)

def log_messages(msg):
    print("log_messages called") #debug purpose
    file = open(logFile,"a")
    file.write(msg)
    file.write(" "+get_curtime()+"\n")
    file.close() 

def load_conversation():
    d = {}
    with codecs.open(actionFile,'r','GBK') as f:
        for line in f:
            (key, val) = line.split('=')
            d[str(key)] = val
    return(d)


bot = Bot()
myself = bot.self
startupMessage='微信机械人启动于'+get_curtime()
bot.file_helper.send(startupMessage)

@bot.register()
def print_messages(msg):
    d=load_conversation()
    print (msg)
    amsg=msg.text
    awho=msg.sender
    awho=str(awho)
    #awho.encode('utf-8') 
    #print(amsg)
    amsg_str=amsg
    amsg_str=amsg_str.decode('utf-8').encode('gb18030') 
    #print(type(awho))
    #print(type(amsg_str))
    #print(type(amsg))
    log_messages(awho+":"+amsg_str)

    key=list(d.keys())
    value=list(d.values())
    amsg=amsg.lower() 

    autoreplyMsg=""
    for i in range(len(key)):
        if ("*autoreply"==key[i]):
            autoreplyMsg=value[i]
            autoreplyMsg.decode('utf-8').encode('gb18030') 
    replyFlag=0
    for i in range(len(key)):
        if (amsg==key[i]):
            print("triggered")
            sentMsg=value[i]
            sentMsg.decode('utf-8').encode('gb18030') 
            msg.reply(sentMsg)
            replyFlag=1
    if  (replyFlag==0 and autoreplyMsg!=""):
        print("autoreplying")
        msg.reply(autoreplyMsg)
        

# The following code is not yet tested
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if 'wxpy' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('哈哈，我自动接受了你的好友请求')


embed()
