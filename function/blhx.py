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
from graia.application.message.elements.internal import At, Image, Plain, Quote, Face
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter

ua = Faker()
headers = {'User-Agent': str(ua.user_agent)}
global null
null = ''
groups = [372733015, 875626950, 862315052, 729801800, 598418410]


async def blhx(app,group):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
    Information = requests.get(url, headers=headers).json()
    judge = Information['data']['cards'][1]

    if judge['desc']['type'] == 1:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        msg = dictInformation['item']['content']
        message = MessageChain.create(
                    [Plain("碧蓝航线b服动态更新\n================\n"), Plain(msg)])
        await app.sendGroupMessage(group, message)

    elif judge['desc']['type'] == 2:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        try:
            if(dictInformation['item']['pictures_count'] == 1):
                pictures = dictInformation['item']['pictures'][0]['img_src']
                flag = 0
            else:
                pictures = dictInformation['item']['pictures']
                flag = 1
                count = dictInformation['item']['pictures_count']
        except:
            pictures = " "
        msgDict = {
            "information": dictInformation['item']['description'], "picture_url": pictures}
        if msgDict['picture_url'] != ' ':
            if flag == 0:
                await app.sendGroupMessage(group, MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"), Plain(msgDict['information']), Image.fromNetworkAddress(msgDict['picture_url'])]))
            elif flag == 1:
                message1 = MessageChain.create(
                    [Plain("碧蓝航线b服动态更新\n================\n"), Plain(msgDict['information'])])
                for i in count:
                    msg = MessageChain.join(
                        [Image.fromNetworkAddress(pictures[i]['img_src'])])
                Msg = MessageChain.join(message1, msg)
                await app.sendGroupMessage(group, Msg)
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"), Plain(msgDict['information'])]))

    elif judge['desc']['type'] == 4:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        pictures = " "
        msgDict = {"information":dictInformation['item']['content'],"picture_url":pictures}
        for group in groups:
            if msgDict['picture_url'] != ' ':
                await app.sendGroupMessage(group,MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information']),Image.fromNetworkAddress(msgDict['picture_url'])]))
            else:
                await app.sendGroupMessage(group,MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information'])]))
    
async def blhxpush(app,preTimestamp):
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
        print("上一个动态的时间戳为：")
        print(preTimestamp)
        print("当前动态的时间戳为：")
        print(timestamp)
        if preTimestamp != timestamp:
            preTimestamp = timestamp
            judge = Information['data']['cards'][1]
            
            if judge['desc']['type'] == 1:
                needInformation = Information['data']['cards'][1]['card']
                dictInformation = eval(needInformation)
                msg = dictInformation['item']['content']
                message = MessageChain.create(
                            [Plain("碧蓝航线b服动态更新\n================\n"), Plain(msg)])
                await app.sendGroupMessage(group, message)

            elif judge['desc']['type'] == 2:
                needInformation = Information['data']['cards'][1]['card']
                dictInformation = eval(needInformation)
                try:
                    if(dictInformation['item']['pictures_count'] == 1):
                        pictures = dictInformation['item']['pictures'][0]['img_src']
                        flag = 0
                    else:
                        pictures = dictInformation['item']['pictures']
                        flag = 1
                        count = dictInformation['item']['pictures_count']
                except:
                    pictures = " "
                msgDict = {"information":dictInformation['item']['description'],"picture_url":pictures}
                for group in groups:
                    if msgDict['picture_url'] != ' ':
                        if flag == 0:
                            await app.sendGroupMessage(group,MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information']),Image.fromNetworkAddress(msgDict['picture_url'])]))
                        elif flag == 1:
                            message1 = MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information'])])
                            for i in count:
                                msg = MessageChain.join([Image.fromNetworkAddress(pictures[i]['img_src'])])
                            Msg = MessageChain.join(message1,msg)
                            await app.sendGroupMessage(group,Msg)
                    else:
                        await app.sendGroupMessage(group,MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information'])]))

            elif judge['desc']['type'] == 4:
                needInformation = Information['data']['cards'][1]['card']
                dictInformation = eval(needInformation)
                pictures = " "
                msgDict = {"information":dictInformation['item']['content'],"picture_url":pictures}
                for group in groups:
                    if msgDict['picture_url'] != ' ':
                        await app.sendGroupMessage(group,MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information']),Image.fromNetworkAddress(msgDict['picture_url'])]))
                    else:
                        await app.sendGroupMessage(group,MessageChain.create([Plain("碧蓝航线b服动态更新\n================\n"),Plain(msgDict['information'])]))

            await asyncio.sleep(60)

        else:
            await asyncio.sleep(60)
            continue
        
        
