#!/usr/bin/python
# -*- coding: UTF-8 -*-
# The program is based on wxpy library. 
# Ref: https://github.com/youfou/wxpy

from wxpy import *
import datetime
import codecs
# FOR PYTHON 27 ON WINDOWS

#Change the default encoding for Chinese characters
#http://blog.csdn.net/a657941877/article/details/9063883
import sys   
reload(sys)   
sys.setdefaultencoding('utf-8')   

logFile   ="winchatbot.log"
actionFile="wintalk.txt"

def get_curtime():
    curtime=datetime.datetime.now().strftime("%I:%M%p on %B %d,%Y")
    return(curtime)

def load_conversation():
    d = {}
    with codecs.open(actionFile,'r','GBK') as f:
        for line in f:
            (key, val) = line.split('=')
            d[str(key)] = val
    return(d)

def log_messages(msg):
    print("log_messages called") #debug purpose
    file = open(logFile,"a")
    file.write(msg)
    file.write(" "+get_curtime()+"\n")
    file.close() 


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
    print (awho)
    #awho.decode('utf-8').encode('gb18030') 
    #amsg=str(unicode(msg.text()))
    print(amsg)
    print(type(awho))
    print(type(amsg))
    log_messages(amsg)
    #amsg.decode('ascii')
    #if amsg == 'test':
    #  msg.reply("搞定")
    if amsg in d : 
      print("triggered")
      sentMsg=d[amsg]
      sentMsg.decode('utf-8').encode('gb18030') 
      msg.reply(sentMsg)

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
