#!/usr/bin/python
# -*- coding: UTF-8 -*-
# The program is based on wxpy library. 
# Ref: https://github.com/youfou/wxpy

from wxpy import *
import datetime

#Mac Version

#Change the default encoding for Chinese characters
#http://blog.csdn.net/a657941877/article/details/9063883
import sys   
reload(sys)   
sys.setdefaultencoding('utf-8')   

logFile="mac_chatbot.log"
actionFile="mac_talk.txt"

def get_curtime():
    curtime=datetime.datetime.now().strftime("%I:%M%p on %B %d,%Y")
    return(curtime)

def load_conversation():
    d = {}
    with open(actionFile) as f:
        for line in f:
            (key, val) = line.split('=')
            d[str(key)] = val
    return(d)

def log_messages(msg):
    #print("log_messages called") #debug purpose
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
    #d = {}
    #with open("talk.txt") as f:
    #    for line in f:
    #        (key, val) = line.split('=')
    #        d[str(key)] = val
    print (msg)
    awho=str(msg.sender)
    #awho.decode('utf-8').encode('gb18030') 
    amsg=msg.text
    amsg=amsg.lower()
    #amsg.decode('utf-8').encode('gb18030') 
    log_messages(awho+":"+amsg)
    if amsg in d : 
      print("triggered")
      msg.reply(d[amsg])

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
