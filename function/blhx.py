import random
import time
import datetime
import asyncio

import requests
from fake_useragent import UserAgent
from faker import Faker
from graia.application import GraiaMiraiApplication, Session
from graia.application.entry import (BotMuteEvent, FriendMessage, GroupMessage,
                                     MemberMuteEvent, MemberUnmuteEvent)
from graia.application.event.lifecycle import ApplicationLaunched
from graia.application.event.messages import TempMessage
from graia.application.event.mirai import BotLeaveEventKick
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain, Quote,Face
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter

ua = Faker()
headers = {'User-Agent': str(ua.user_agent)}
global null
null = ''
groups = [372733015,875626950,766517688,862315052]

def blhx():
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
    Information = requests.get(url,headers = headers).json()
    judge = Information['data']['cards'][1]

    if judge['desc']['type'] == 2:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        try:
            if(dictInformation['item']['pictures_count'] == 1):
                pictures = dictInformation['item']['pictures'][0]['img_src']
                print(pictures)
        except:
            pictures = " "
        return {"information":dictInformation['item']['description'],"picture_url":pictures}


    elif judge['desc']['type'] == 4:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        pictures = " "
        return {"information":dictInformation['item']['content'],"picture_url":pictures}
    
async def blhxpush(app):
    await asyncio.sleep(10)
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
    Information = requests.get(url,headers = headers).json()
    while(True):
        t = time.time()
        t = int(t)
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
        Information = requests.get(url,headers = headers).json()
        try:
            timestamp = Information['data']['cards'][1]['desc']['timestamp']
        except:
            timestamp = 0
        print("当前时间戳为：")
        print(t)
        print("最新动态的时间戳为：")
        print(timestamp)
        print("两者差值为：")
        print(t - timestamp)
        if t - timestamp <= 66:
            judge = Information['data']['cards'][1]
            if judge['desc']['type'] == 2:
                needInformation = Information['data']['cards'][1]['card']
                dictInformation = eval(needInformation)
                try:
                    if(dictInformation['item']['pictures_count'] == 1):
                        pictures = dictInformation['item']['pictures'][0]['img_src']
                except:
                    pictures = " "
                msgDict = {"information":dictInformation['item']['description'],"picture_url":pictures}
                for group in groups:
                    if msgDict['picture_url'] != ' ':
                        await app.sendGroupMessage(group,MessageChain.create([Plain(msgDict['information']),Image.fromNetworkAddress(msgDict['picture_url'])]))
                    else:
                        await app.sendGroupMessage(group,MessageChain.create([Plain(msgDict['information'])]))

            elif judge['desc']['type'] == 4:
                needInformation = Information['data']['cards'][1]['card']
                dictInformation = eval(needInformation)
                pictures = " "
                msgDict = {"information":dictInformation['item']['content'],"picture_url":pictures}
                for group in groups:
                    if msgDict['picture_url'] != ' ':
                        await app.sendGroupMessage(group,MessageChain.create([Plain(msgDict['information']),Image.fromNetworkAddress(msgDict['picture_url'])]))
                    else:
                        await app.sendGroupMessage(group,MessageChain.create([Plain(msgDict['0information'])]))

            await asyncio.sleep(60)

        else:
            await asyncio.sleep(60)
            continue
        
        
