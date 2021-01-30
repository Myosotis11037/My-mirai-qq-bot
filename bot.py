import asyncio
import datetime
import json
import operator
import random
import requests
from re import escape
from typing import Dict, Optional

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

from function.bilibili import bvcrawler
from function.bilibili import avcrawler
from function.time import bell,clock
from function.touhou import Touhou
from function.blhx import blhx
from function.blhx import blhxpush

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="HolaisanKaguya", # 填入 authKey
        account=3304895821, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

@bcc.receiver(GroupMessage)
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    if message.asDisplay() == "help":
        sstr = "目前已经公开的功能有：" + "\n\n" 
        sstr += "①打招呼功能，输入hi说不定可以得到妹妹的回应哦~" + "\n\n"
        sstr += "②查bv号和av号的功能，能够显示视频的详细信息~" + "\n\n"
        sstr += "③随机提供涩图的功能，输入‘色图时间’或者‘来点涩图’就可以随机发送一张图片了~" + "\n\n"
        sstr += "④整点报时功能~\n\n"
        sstr += "⑤提供b站车万区周榜功能~\n\n"
        sstr += "⑥碧蓝航线实时推送功能，并且输入'碧蓝航线最新动态'可以得到碧蓝航线官方账号发送的最新动态哦~\n"
        sstr += "凛夜sama赛高！（不要忘了所有的功能都是凛夜亲手敲的代码哦）"
        await app.sendGroupMessage(group,MessageChain.create([Plain(sstr)]))

    if message.asDisplay() == "hi":
        if(member.id == 5980403):
            await app.sendGroupMessage(group,MessageChain.create([At(5980403),Plain(" 哥哥爱死你了mua")]))
        elif(member.id == 349468958):
            await app.sendGroupMessage(group,MessageChain.create([Plain("哥哥我也爱你呢❤")]))
        elif(member.id == 865734287):
            await app.sendGroupMessage(group,MessageChain.create([Plain("mu..(害怕)mua?"),Face(faceId=111)]))
        elif(member.id == 744938425):
            await app.sendGroupMessage(group,MessageChain.create([At(744938425),Plain(" 欧尼酱要吃饭呢，要洗澡呢，还是要先吃我呢"),Face(faceId=111)]))
        else:
            await app.sendGroupMessage(group,MessageChain.create([At(member.id),Plain("hi~")]))
    
    if message.asDisplay() == "晚安":
        if(member.id == 5980403):
            await app.sendGroupMessage(group,MessageChain.create([At(5980403),Plain(" 哥哥晚安"),Face(faceId=75)]))
        else:
            await app.sendGroupMessage(group,MessageChain.create([At(member.id),Plain(" 晚安~")]))

    if message.asDisplay() == "草" or message.asDisplay() == "艹":
        await app.sendGroupMessage(group,MessageChain.create([Plain("草")]))

    if(member.id != 2083664136 and member.id != 2079373402):
        if message.asDisplay().startswith("BV"):
            videoInformation = bvcrawler(message.asDisplay())
            await app.sendGroupMessage(group,MessageChain.create([Plain(videoInformation)]))
        elif message.asDisplay().startswith("AV") or message.asDisplay().startswith("av"):
            videoInformation = avcrawler(message.asDisplay())
            await app.sendGroupMessage(group,MessageChain.create([Plain(videoInformation)]))

    if message.asDisplay() == "色图时间" or message.asDisplay() == "来点涩图" or message.asDisplay() == "来点色图":
        url = "https://api.nmb.show/1985acg.php"

        try:
            await app.sendGroupMessage(group, MessageChain.create([Image.fromNetworkAddress(url)]))
        except:
            await app.sendGroupMessage(group,MessageChain.create([Plain("该图片无法显示qwq"),Face(faceId=107)]))

    if message.asDisplay() == "车万周榜" or message.asDisplay() == "东方周榜":
        msg = Touhou()
        await app.sendGroupMessage(group,MessageChain.create([Plain(msg)]))
    
    if message.asDisplay() == "维护" and member.id == 5980403:
        msg = "就算是机器人的妹妹我也要休息了呢qwq，凛夜哥哥要对我进行功能维护了，大家好好期待吧"
        groups = [372733015,766517688,875626950,862315052]
        for group in groups:
            await app.sendGroupMessage(group,MessageChain.create([Plain(msg)]))

    if message.asDisplay() == "碧蓝航线最新动态":
        msgDict = blhx()
        if msgDict['picture_url'] != ' ':
            await app.sendGroupMessage(group,MessageChain.create([Plain(msgDict['information']),Image.fromNetworkAddress(msgDict['picture_url'])]))
        else:
            await app.sendGroupMessage(group,MessageChain.create([Plain(msgDict['information'])]))


@bcc.receiver(ApplicationLaunched)
async def repeat(app:GraiaMiraiApplication):
    asyncio.create_task(clock(app))
    asyncio.create_task(blhxpush(app))
    


app.launch_blocking()